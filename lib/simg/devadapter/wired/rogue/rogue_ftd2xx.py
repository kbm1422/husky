#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger(__name__)

import threading
import ftd2xx
from simg import fs


class FlashOperationCode(object):
    AAIProgram = 0x25,
    ERASE = 0x21,
    FINISH = 0x24,
    GetChipID = 0x26,
    PROGRAM = 0x22,
    VERIFY = 0x23


class RogueAdapter(object):
    def __init__(self, comport, logname=None):
        self._shouldstop = threading.Event()
        self._ftdi = None
        self._rw_mutex = threading.RLock()

        self._logname = None
        if logname:
            self.setLogFilename(logname)
        self._comport = comport
        self._is_opened = False

    def isOpened(self):
        return self._is_opened

    def open(self):
        if self._comport is None:
            raise ValueError
        self._ftdi = ftd2xx.openEx(self._comport)
        self._ftdi.setBaudRate(57600)
        self._is_opened = True
        self._shouldstop.clear()
        threading.Thread(target=self._getting_log_output).start()

    def _getting_log_output(self):
        while not self._shouldstop.is_set():
            with self._rw_mutex:
                data = self._ftdi.read(self._ftdi.getQueueStatus())
            self._process_log_record(data)
            time.sleep(0.1)

    def _process_log_record(self, data):
        if data:
            data = data.replace("\r", "")
            logger.debug("firmware log output: \n%s", data)
            if self._logname:
                with open(self._logname, "a") as logfile:
                    logfile.write(data)

    def close(self):
        self._shouldstop.set()
        self._is_opened = False

    def read(self, size=None, timeout=None):
        timeout = timeout or 0
        if size is not None:
            with self._rw_mutex:
                self._ftdi.setTimeouts(int(timeout*1000), 0)
                data = self._ftdi.read(size)
                self._ftdi.setTimeouts(0, 0)
                return data
        else:
            data = ""
            starttime = time.time()
            with self._rw_mutex:
                while True:
                    data += self._ftdi.read(self._ftdi.getQueueStatus())
                    if time.time() - starttime >= timeout:
                        break
                return data

    def write(self, data, timeout=None):
        timeout = timeout or 0
        with self._rw_mutex:
            self._ftdi.setTimeouts(0, int(timeout*1000))
            self._ftdi.write(str(data))
            self._ftdi.setTimeouts(0, 0)

    def sendMSCCommand(self, type, byte):
        data = bytearray(5)
        data[0] = 0xff
        data[1] = 0x10
        data[2] = 0x02
        data[3] = type
        data[4] = byte
        with self._rw_mutex:
            self.write(data)
            s = self.read(timeout=1.0)
            lines = s.split("\r\n")
            ret = lines[1][0:3]
            lines[1] = lines[1][3:]
            self._process_log_record("\r\n".join(lines))

    def rcp(self, byte):
        self.sendMSCCommand(0x10, byte)

    def rbp(self, byte):
        self.sendMSCCommand(0x22, byte)

    def ucp(self, byte):
        self.sendMSCCommand(0x30, byte)

    def readRegister(self, page_id, offset):
        #clean and handle the buffer as logs
        self._process_log_record(self.read(self._ftdi.getQueueStatus()))

        logger.info("read register '0x%X' from page '0x%X'", offset, page_id)
        data = bytearray(6)
        data[0] = 0xff
        data[1] = 0xe0
        data[2] = len(data) - 3
        data[3] = page_id
        data[4] = offset
        data[5] = 8 >> 3
        logger.debug("send: %r", data)
        with self._rw_mutex:
            self.write(str(data))
            resp = self.read(4, timeout=5.0)
        logger.debug("recv: %r", resp)

        value = ord(resp[3])
        logger.info("value: 0x%X", value)
        return value

    def writeRegister(self, page_id, offset, value):
        logger.info("write register on page '0x%X': offset='0x%X', value='0x%X' ", page_id, offset, value)
        data = bytearray(6 + (8 >> 3))
        data[0] = 0xff
        data[1] = 0x60
        data[2] = len(data) - 3
        data[3] = page_id
        data[4] = offset
        data[5] = 8 >> 3
        for i in range(0, 8 >> 3):
            data[6+i] = value
            value >>= 8
        logger.debug("send: %r", data)
        self.write(str(data))

    def setLogFilename(self, logname):
        logger.info("set log filename to: %s", logname)
        fs.touch(logname)
        self._logname = logname

    def upgradeFirmware(self, filename):
        logger.info("upgrade firmware with path: %s", filename)
        with open(filename, "rb") as fw:
            flash = fw.read()
        total_length = len(flash)

        def program():
            logger.debug("programing start")
            index = 0
            slice_length = 0x100
            process = None
            for _ in range(total_length/slice_length):
                self._spi_flash_write_block(flash, index, slice_length)
                index += slice_length

                prev_process = process
                process = int(round(float(index)/float(total_length), 2) * 100)
                if (process % 5) == 0 and process != prev_process:
                    logger.debug("programing process: %s%%", process)
            self._spi_flash_write_block(flash, index, total_length % slice_length)
            logger.debug("programing done")

        def verify():
            logger.debug("verifing start")
            index = 0
            slice_length = 0x80
            process = None
            embeded = []
            for _ in range(total_length/slice_length):
                embeded += self._spi_flash_read_block(index, slice_length)
                index += slice_length

                prev_process = process
                process = int(round(float(index)/float(total_length), 2) * 100)
                if (process % 5) == 0 and process != prev_process:
                    logger.debug("verifing process: %s%%", process)
            embeded += self._spi_flash_read_block(index, total_length % slice_length)

            chkcode1 = 0
            for i in range(0x9000, 0x19000):
                chkcode1 += ord(embeded[i])

            chkcode2 = ord(embeded[0x19000]) | (ord(embeded[0x19001]) << 8) | (ord(embeded[0x19002]) << 0x10) | (ord(embeded[0x19003]) << 0x18)
            if (~chkcode1 + 1) != chkcode2:
                raise Exception("verify failed")
            logger.debug("verifing done")

        self._spi_flash_erase()
        program()
        verify()
        self._spi_flash_finish()
        logger.info("upgrade firmware finished")

    def upgradeHostSoftware(self, filename):
        raise NotImplementedError

    def _spi_flash_erase(self):
        logger.info("start to erase flash")
        data = bytearray()
        data.append(0x80)
        data.append(0x21)
        data.append(2)
        data.append(0)
        data.append(0x60)
        self._spi_flash_write(data)
        logger.info("spi_flash_erase done")

    def _spi_flash_read_block(self, index, length):
        data = bytearray()
        data.append(0x80)
        data.append(0x23)
        data.append(7)
        data.append(0)
        data.append(index & 0xff)
        data.append((index >> 8) & 0xff)
        data.append((index >> 0x10) & 0xff)
        data.append(length)
        data.append(0)
        data.append(0x60)
        with self._rw_mutex:
            attempt = 3
            while True:
                self.write(str(data))
                if ord(self.read(1)) == 0x80:
                    buff = self.read(130)
                    if ord(buff[0]) == data[1] and ord(buff[1]) == 0x80:
                        return buff[2:]

                attempt -= 1
                if attempt == 0:
                    raise Exception("reach the max attempt number")
                logger.debug("retry sending data: %r", data)

    def _spi_flash_write_block(self, flash, index, length):
        data = bytearray()
        data.append(0x80)
        data.append(0x22)
        data.append((length+7) % 0x100)
        data.append((length + 7) >> 8)
        data.append(index & 0xff)
        data.append((index >> 8) & 0xff)
        data.append((index >> 0x10) & 0xff)
        data.append(length % 0x100)
        data.append(length >> 8)
        data += flash[index:index+length]
        data.append(0x60)
        self._spi_flash_write(data)

    def _spi_flash_finish(self):
        logger.info("finish flash")
        data = bytearray()
        data.append(0x80)
        data.append(0x24)
        data.append(2)
        data.append(0)
        data.append(0x60)
        self._spi_flash_write(data)

    def _spi_flash_write(self, data, attempt=3):
        with self._rw_mutex:
            while True:
                self.write(str(data))
                if ord(self.read(1)) == 0x80:
                    buff = self.read(2)
                    if ord(buff[0]) == data[1] and ord(buff[1]) == 0:
                        break

                attempt -= 1
                if attempt == 0:
                    raise Exception("reach the max attempt number")
                logger.debug("retry sending data: %r", data)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)-15s [%(levelname)-8s] - %(message)s'
    )
    import time
    from simg.util.powerswitch import PowerSwitchOutlet

    # adpt.open()
    # adpt.setLogFilename(r"H:\temp.log")
    # adpt.read_register(0x20, 0x0B)
    # adpt.read_register(0x20, 0x0C)
    #
    # psoutlet = PowerSwitchOutlet("192.168.1.110", 1)
    # psoutlet.turnoff()
    # time.sleep(1)
    # psoutlet.turnon()
    # adpt.write_register(0x70, 0x0F, 0x80)
    # adpt.read_register(0x20, 0x0B)
    # adpt.read_register(0x20, 0x0C)
    # adpt.close()

    rogue = RogueAdapter("A", r"H:\rogue.log")
    rogue.open()

    # psoutlet = PowerSwitchOutlet("192.168.1.110", 1)
    # psoutlet.turnoff()
    # time.sleep(1)
    # psoutlet.turnon()
    try:
        #rogue.spi_flash_erase()
        # rogue.upgradeFirmware(r"H:\wired\products\Rogue\firmware\SiI9679_FW_1.01.13_SVN21903_20140507.bin")
        # psoutlet = PowerSwitchOutlet("192.168.1.110", 1)
        # psoutlet.turnoff()
        # time.sleep(1)
        # psoutlet.turnon()
        rogue.rcp(0x01)
        rogue.rbp(0x02)
        rogue.ucp(0x03)
    except ftd2xx.DeviceError:
        logger.exception("")
    finally:
        rogue.close()
    # with open(r"H:\wired\products\Rogue\firmware\SiI9679_FW_1.01.13_SVN21903_20140507.bin", "rb") as f:
    #     flash = f.read()
    #     print len(flash)
        # print repr(flash[0:10])
        # print repr(flash[10:20])
        # index = 0
        # length = 0x100
        # for _ in range(2):
        #     if flash:
        #         rogue.spi_flash_write_block(flash, index, length)
        #         index += length
        #     else:
        #         break

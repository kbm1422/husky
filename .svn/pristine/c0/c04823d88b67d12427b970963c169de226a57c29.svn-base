#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger(__name__)

import time
import ctypes
import threading

from simg.devadapter import BaseDeviceAdapter, DeviceAdapterError, DeviceEndType
from simg.devadapter.logsubject import SerialLogSubject
from simg.pattern.observer import BaseSubject, BaseListener
from simg.devadapter.wired.base import MscMessage, Mhl3Interface
from simg.devadapter.wired.aardvark_py import array_u16, array_u32, aa_find_devices_ext

import os
ctypes.CDLL(os.path.join(os.path.dirname(__file__), 'Sii9777RxLib.dll'))
from Sii9777RxLib import *


MAX_NUM_ADAPTERS = 10


def find_aa_devices():
    devices = array_u16(MAX_NUM_ADAPTERS)
    unique_ids = array_u32(MAX_NUM_ADAPTERS)
    num, devs, ids = aa_find_devices_ext(devices, unique_ids)
    ports = dict(zip(ids.tolist(), devs.tolist())[0:num])
    logger.debug("aardvark devices: %s", ports)
    return ports


def get_port_by_uid(uid):
    return find_aa_devices()[uid]


class BostonDeviceAdapter(BaseDeviceAdapter, Mhl3Interface):
    """
    The device adapter must be closed with reversed sequence with creation sequence.
    Otherwise it will cause the Sii9777RxLib.dll release memory incorrectly.
    """
    def __init__(self, comport=None, devport=None, **kwargs):
        super(BostonDeviceAdapter, self).__init__(**kwargs)
        self.devport = None if devport is None else get_port_by_uid(long(devport.replace("-", "")))
        self.comport = comport
        self.log_subject = SerialLogSubject(comport, 115200)
        self.evt_subject = BostonDriverEventSubject(self.__str__())
        self.drv_instance = None
        self.lock = threading.Lock()
        self.__thread = None
        self.__should_stop = threading.Event()

    def __str__(self):
        return "<BostonDeviceAdapter(comport:%s, devport:%s)>" % (self.comport, self.devport)

    @property
    def end_type(self):
        if self.id == 0x9777:
            return DeviceEndType.SOURCE
        else:
            raise ValueError

    def open(self):
        if self.comport is not None:
            self.log_subject.open()

        self.__should_stop.clear()
        if self.devport is not None:
            self.__thread = threading.Thread(target=self.__init_and_get_interrupt_for_ever)
            self.__thread.name = threading.current_thread().name
            self.__thread.start()
            time.sleep(5.0)

            if self.drv_instance is None:
                raise DeviceAdapterError("Create Sii9777 instance failed")

    def close(self):
        self.__should_stop.set()
        if self.__thread is not None:
            self.__thread.join()
            self.__thread = None

        if self.comport is not None:
            self.log_subject.close()

    def send_msc_message(self, message):
        logger.debug("%s send msc message: %s", self, message)
        msg = Sii9777MscCmd_t()
        msg.subCmd = Sii9777MscSubCmd_t(message.type)
        msg.codeValue = message.code
        with self.lock:
            retcode = Sii9777CbusMscMsgSend(self.drv_instance, ctypes.byref(msg))
        return retcode

    def recv_msc_message(self):
        msg = Sii9777MscCmd_t()
        with self.lock:
            retcode = Sii9777CbusMscMsgReceive(self.drv_instance, ctypes.byref(msg))
        if retcode == 0:
            message = MscMessage(msg.subCmd, msg.codeValue)
            logger.debug("%s recv msc message: %s", self, message)
            return message
        else:
            logger.debug("%s recv msc message error", self)
            return None

    def set_local_devcap(self, data):
        logger.debug("%s set local devcap: %s", self, data)
        pData = (uint8_t * 16)()
        for index in range(16):
            pData[index] = data[index]
        offset = uint8_t(0)
        length = uint8_t(16)
        with self.lock:
            retcode = Sii9777CbusLocalDevcapSet(self.drv_instance, pData, offset, length)
        if retcode != 0:
            raise DeviceAdapterError("call API Sii9777CbusLocalDevcapSet failed.")

    def get_local_devcap(self):
        pData = (uint8_t * 16)()
        offset = uint8_t(0)
        length = uint8_t(16)
        with self.lock:
            retcode = Sii9777CbusLocalDevcapGet(self.drv_instance, pData, offset, length)
        if retcode != 0:
            raise DeviceAdapterError("call API Sii9777CbusLocalDevcapGet failed.")
        devcap = [pData[index] for index in range(16)]
        logger.debug("%s get local devcap: %s", self, devcap)
        return devcap

    def set_local_x_devcap(self, data):
        logger.debug("%s set local x devcap: %s", self, data)
        pData = (uint8_t * 4)()
        for index in range(4):
            pData[index] = data[index]
        offset = uint8_t(0)
        length = uint8_t(4)
        with self.lock:
            retcode = Sii9777CbusLocalXDevcapSet(self.drv_instance, pData, offset, length)
        if retcode != 0:
            raise DeviceAdapterError("call API Sii9777CbusLocalXDevcapSet failed.")

    def get_local_x_devcap(self):
        pData = (uint8_t * 4)()
        offset = uint8_t(0)
        length = uint8_t(4)

        with self.lock:
            retcode = Sii9777CbusLocalXDevcapGet(self.drv_instance, pData, offset, length)
        if retcode != 0:
            raise DeviceAdapterError("call API Sii9777CbusLocalXDevcapGet failed.")
        x_devcap = [pData[index] for index in range(4)]
        logger.debug("%s get local x devcap: %s", self, x_devcap)
        return x_devcap

    def get_remote_devcap(self):
        raise NotImplementedError

    def get_remote_x_devcap(self):
        raise NotImplementedError

    def send_devcap_change_command(self):
        with self.lock:
            retcode = Sii9777CbusDcapChgSend(self.drv_instance)
        if retcode != 0:
            raise DeviceAdapterError("call API Sii9777CbusDcapChgSend failed.")

    def set_hpd(self, port, value):
        with self.lock:
            Sii9777HpdSet(self.drv_instance, Sii9777RxPort_t(port), ctypes.byref(bool_t(value)))

    def get_hpd(self, port):
        state = bool_t()
        with self.lock:
            Sii9777HpdGet(self.drv_instance, Sii9777RxPort_t(port), ctypes.byref(state))
        return state.value

    @staticmethod
    def convert_edid_list2ubytes(l):
        length = len(l)
        pData = (uint8_t * length)()
        for index in range(length):
            pData[index] = l[index]
        return pData

    @staticmethod
    def convert_edid_ubytes2list(ubytes):
        return [ubytes[index] for index in range(len(ubytes))]

    def get_edid(self, port, offset=0, length=256):
        pData = (uint8_t * length)()
        with self.lock:
            Sii9777EdidQuery(self.drv_instance, Sii9777RxPort_t(port), uint16_t(offset), pData, uint16_t(length))
        logger.debug("SII9777_RX_PORT__%s EDID: %s", port, ["0x%02X" % pData[index] for index in range(length)])
        return self.convert_edid_ubytes2list(pData)

    def __init_flash(self, operation, target):
        logger.debug("Sii9777FlashInit: operation=%s, target=%s", operation, target)
        with self.lock:
            Sii9777FlashInit(self.drv_instance, operation, target)

        while True:
            pStatus = Sii9777FileStatus_t()
            with self.lock:
                Sii9777FlashStatusQuery(self.drv_instance, ctypes.byref(pStatus))
            if pStatus.value == SII9777_FILE_STATUS__READY:
                break
            elif pStatus.value == SII9777_FILE_STATUS__IN_PROGRESS:
                time.sleep(0.5)
                continue
            elif pStatus.value == SII9777_FILE_STATUS__FAILURE:
                raise DeviceAdapterError("Sii9777FlashInit failed.")
            else:
                raise DeviceAdapterError("Unsupported status value %s" % pStatus.value)

    @staticmethod
    def update_flash_checksum(flash):
        sum = 0
        end_addr = 0x6000 + 0x40000
        for i in range(0x6000, end_addr):
            sum += ord(flash[i])
        checksum = 0 - sum

        flash[0x0000001A] = chr(checksum & 0xFF)
        flash[0x0000001A + 1] = chr((checksum >> 8) & 0xFF)
        flash[0x0000001A + 2] = chr((checksum >> 16) & 0xFF)
        flash[0x0000001A + 3] = chr((checksum >> 24) & 0xFF)

    def update_flash_full_device(self, filename):
        self.__init_flash(SII9777_FILE_OPERATION__WRITE, SII9777_FILE_TARGET__FULL_DEVICE)

        with open(filename, "rb") as f:
            flash = f.read()
        logger.debug("set RX0-RX3 HPD to True and update flash checksum")
        l = list(flash)
        l[0x0000DEBB] = '\x01'
        l[0x0000DEBC] = '\x01'
        l[0x0000DEBD] = '\x01'
        l[0x0000DEBE] = '\x01'
        flash = l
        self.update_flash_checksum(flash)

        logger.debug("programing start")

        index = 0
        total_length = len(flash)
        slice_length = 256
        process = None
        for i in range(total_length/slice_length):
            self.__write_flash_block(flash[index:(i+1)*slice_length])
            index += slice_length

            prev_process = process
            process = int(round(float(index)/float(total_length), 2) * 100)
            if (process % 5) == 0 and process != prev_process:
                logger.debug("programing process: %s%%", process)
        if total_length % slice_length > 0:
            self.__write_flash_block(flash[index:-1], )
        logger.debug("programing done")

        with self.lock:
            Sii9777FirmwareRestart(self.drv_instance)
        time.sleep(1.0)

        while self.__query_boot_status() == SII9777_BOOT_STAT__IN_PROGRESS:
            time.sleep(0.5)

        if self.__query_boot_status() == SII9777_BOOT_STAT__FAILURE:
            raise DeviceAdapterError("upgrade firmware failed")
        logger.info("upgrade firmware successfully")

    update_firmware = update_flash_full_device

    def __write_flash_block(self, data):
        logger.debug("write flash block: %r", data)
        length = len(data)
        buff = (uint8_t*length)()
        for i in range(length):
            buff[i] = uint8_t(ord(data[i]))

        with self.evt_subject.listen(SII9777_EVENT_FLAGS__FLASH_DONE) as listener:
            with self.lock:
                Sii9777FlashUpdate(self.drv_instance, buff, length)
            event = listener.get(timeout=3.0)
            if event is None:
                raise DeviceAdapterError("Sii9777FlashUpdate failed.")

    def __query_boot_status(self):
        boot_state = Sii9777BootStat_t()
        with self.lock:
            Sii9777BootStatusQuery(self.drv_instance, ctypes.byref(boot_state))
        return boot_state.value

    def __init_and_get_interrupt_for_ever(self):
        # if not SiiHalAardvarkCreate()
        if not SiiPlatformCreate(self.devport):
            raise DeviceAdapterError("ERROR: I2c not available")

        config = Sii9777Config_t()
        config.pNameStr = "9777-Rx"
        config.bDeviceReset = bool_t(True)

        func = Sii9777EventCallbackFunc_t(self.evt_subject.event_callback)
        self.drv_instance = Sii9777Create(self.devport, func, ctypes.byref(config))
        if not self.drv_instance:
            raise DeviceAdapterError("Call driver api SiiDrvAdaptCreate failed!!!")

        while True:
            status = Sii9777BootStat_t()
            with self.lock:
                Sii9777BootStatusQuery(self.drv_instance, ctypes.byref(status))
            if status.value == SII9777_BOOT_STAT__IN_PROGRESS:
                time.sleep(0.1)
                continue
            elif status.value == SII9777_BOOT_STAT__FAILURE:
                raise ValueError("Sii9777BootStatus: SII9777_BOOT_STAT__FAILURE")
            elif status.value == SII9777_BOOT_STAT__SUCCESS:
                break
            else:
                raise ValueError("Sii9777BootStatus not in (0, 1, 2)")

        mask = Sii9777EventFlags_t(SII9777_EVENT_FLAGS__ALL)
        with self.lock:
            Sii9777EventFlagsMaskSet(self.drv_instance, ctypes.byref(mask))

        while not self.__should_stop.is_set():
            with self.lock:
                #logger.debug("Call SiiHalAardvarkInterruptQuery")
                #if SiiHalAardvarkInterruptQuery():
                if SiiPlatformInterruptQuery(self.devport):
                    Sii9777Handle(self.drv_instance)
            time.sleep(0.1)

        with self.lock:
            Sii9777Delete(self.drv_instance)
            #SiiHalAardvarkDelete()
            SiiPlatformDelete(self.devport)


DRIVER_EVENT_MAPPER = {
    SII9777_EVENT_FLAGS__BOOT_DONE: "SII9777_EVENT_FLAGS__BOOT_DONE",                                       # 1
    SII9777_EVENT_FLAGS__FLASH_DONE: "SII9777_EVENT_FLAGS__FLASH_DONE",                                     # 2
    SII9777_EVENT_FLAGS__GPIO_CHNG: "SII9777_EVENT_FLAGS__GPIO_CHNG",                                       # 4
    SII9777_EVENT_FLAGS__PLUS_5V_CHNG: "SII9777_EVENT_FLAGS__PLUS_5V_CHNG",                                 # 16
    SII9777_EVENT_FLAGS__EDID_CHNG: "SII9777_EVENT_FLAGS__EDID_CHNG",                                       # 32
    SII9777_EVENT_FLAGS__HPD_CHNG: "SII9777_EVENT_FLAGS__HPD_CHNG",                                         # 64
    SII9777_EVENT_FLAGS__AV_LINK_CHNG: "SII9777_EVENT_FLAGS__AV_LINK_CHNG",                                 # 128
    SII9777_EVENT_FLAGS__AV_MUTE_CHNG: "SII9777_EVENT_FLAGS__AV_MUTE_CHNG",                                 # 256
    SII9777_EVENT_FLAGS__VIDEO_TIMING_CHNG: "SII9777_EVENT_FLAGS__VIDEO_TIMING_CHNG",                       # 512
    SII9777_EVENT_FLAGS__VIDEO_FMT_CHNG: "SII9777_EVENT_FLAGS__VIDEO_FMT_CHNG",                             # 1024
    SII9777_EVENT_FLAGS__AUDIO_FMT_CHNG: "SII9777_EVENT_FLAGS__AUDIO_FMT_CHNG",                             # 2048
    SII9777_EVENT_FLAGS__ISRC_CHNG: "SII9777_EVENT_FLAGS__ISRC_CHNG",                                       # 4096
    SII9777_EVENT_FLAGS__ACP_CHNG: "SII9777_EVENT_FLAGS__ACP_CHNG",                                         # 8192
    SII9777_EVENT_FLAGS__SPD_CHNG: "SII9777_EVENT_FLAGS__SPD_CHNG",                                         # 16384
    SII9777_EVENT_FLAGS__HDCP_STREAM_CHNG: "SII9777_EVENT_FLAGS__HDCP_STREAM_CHNG",                         # 32768
    SII9777_EVENT_FLAGS__HDCP_STATUS_CHNG: "SII9777_EVENT_FLAGS__HDCP_STATUS_CHNG",                         # 65536
    SII9777_EVENT_FLAGS__CD_SENSE_CHNG: "SII9777_EVENT_FLAGS__CD_SENSE_CHNG",                               # 131072
    SII9777_EVENT_FLAGS__MHL_VERSION_CHNG: "SII9777_EVENT_FLAGS__MHL_VERSION_CHNG",                         # 262144
    SII9777_EVENT_FLAGS__CBUS_EVENT: "SII9777_EVENT_FLAGS__CBUS_EVENT",                                     # 1048576
    SII9777_EVENT_FLAGS__VBUS_REQUEST: "SII9777_EVENT_FLAGS__VBUS_REQUEST",                                 # 2097152
    SII9777_EVENT_FLAGS__DUAL_LINK_CHNG: "SII9777_EVENT_FLAGS__DUAL_LINK_CHNG",                             # 4194304
}


class BostonDriverEventListener(BaseListener):
    def __repr__(self):
        return "<%s %s(%s)>" % (self.__class__.__name__, DRIVER_EVENT_MAPPER[self.keyword], self.keyword)


class BostonDriverEventSubject(BaseSubject):
    Listener = BostonDriverEventListener

    def __init__(self, name):
        super(BostonDriverEventSubject, self).__init__()
        self.__name = name

    def __notify(self, etype, flag):
        logger.debug("%s RECV EVENT: %s", self.__name, DRIVER_EVENT_MAPPER[etype])
        for listener in self._listeners:
            if listener.keyword == etype:
                listener.queue.put(flag)

    def event_callback(self, instance, flag):
        if flag & SII9777_EVENT_FLAGS__BOOT_DONE:
            self.__notify(SII9777_EVENT_FLAGS__BOOT_DONE, flag)

        if flag & SII9777_EVENT_FLAGS__FLASH_DONE:
            self.__notify(SII9777_EVENT_FLAGS__FLASH_DONE, flag)

        if flag & SII9777_EVENT_FLAGS__GPIO_CHNG:
            self.__notify(SII9777_EVENT_FLAGS__GPIO_CHNG, flag)

        if flag & SII9777_EVENT_FLAGS__PLUS_5V_CHNG:
            self.__notify(SII9777_EVENT_FLAGS__PLUS_5V_CHNG, flag)

        if flag & SII9777_EVENT_FLAGS__EDID_CHNG:
            self.__notify(SII9777_EVENT_FLAGS__EDID_CHNG, flag)

        if flag & SII9777_EVENT_FLAGS__HPD_CHNG:
            self.__notify(SII9777_EVENT_FLAGS__HPD_CHNG, flag)

        if flag & SII9777_EVENT_FLAGS__AV_LINK_CHNG:
            self.__notify(SII9777_EVENT_FLAGS__AV_LINK_CHNG, flag)

        if flag & SII9777_EVENT_FLAGS__AV_MUTE_CHNG:
            self.__notify(SII9777_EVENT_FLAGS__AV_MUTE_CHNG, flag)

        if flag & SII9777_EVENT_FLAGS__VIDEO_TIMING_CHNG:
            self.__notify(SII9777_EVENT_FLAGS__VIDEO_TIMING_CHNG, flag)

        if flag & SII9777_EVENT_FLAGS__VIDEO_FMT_CHNG:
            self.__notify(SII9777_EVENT_FLAGS__VIDEO_FMT_CHNG, flag)

        if flag & SII9777_EVENT_FLAGS__AUDIO_FMT_CHNG:
            self.__notify(SII9777_EVENT_FLAGS__AUDIO_FMT_CHNG, flag)

        if flag & SII9777_EVENT_FLAGS__ISRC_CHNG:
            self.__notify(SII9777_EVENT_FLAGS__ISRC_CHNG, flag)

        if flag & SII9777_EVENT_FLAGS__ACP_CHNG:
            self.__notify(SII9777_EVENT_FLAGS__ACP_CHNG, flag)

        if flag & SII9777_EVENT_FLAGS__SPD_CHNG:
            self.__notify(SII9777_EVENT_FLAGS__SPD_CHNG, flag)

        if flag & SII9777_EVENT_FLAGS__HDCP_STREAM_CHNG:
            self.__notify(SII9777_EVENT_FLAGS__HDCP_STREAM_CHNG, flag)

        if flag & SII9777_EVENT_FLAGS__HDCP_STATUS_CHNG:
            self.__notify(SII9777_EVENT_FLAGS__HDCP_STATUS_CHNG, flag)

        if flag & SII9777_EVENT_FLAGS__CD_SENSE_CHNG:
            self.__notify(SII9777_EVENT_FLAGS__CD_SENSE_CHNG, flag)

        if flag & SII9777_EVENT_FLAGS__MHL_VERSION_CHNG:
            self.__notify(SII9777_EVENT_FLAGS__MHL_VERSION_CHNG, flag)

        if flag & SII9777_EVENT_FLAGS__CBUS_EVENT:
            self.__notify(SII9777_EVENT_FLAGS__CBUS_EVENT, flag)

        if flag & SII9777_EVENT_FLAGS__VBUS_REQUEST:
            self.__notify(SII9777_EVENT_FLAGS__VBUS_REQUEST, flag)

        if flag & SII9777_EVENT_FLAGS__DUAL_LINK_CHNG:
            self.__notify(SII9777_EVENT_FLAGS__DUAL_LINK_CHNG, flag)


# from simg.devadapter.wired.aardvark_py import *
# class __Obsolete_BostonDeviceAdapter(object):
#     DEVICE_ID = 0x40
#     ADDRESS_WIDTH = 16
#
#     def __init__(self, type, id, comport, devport=None):
#         self.type = type
#         self.id = id if isinstance(id, int) else int(id, 16)
#         self.devport = None if devport is None else int(devport)
#         self._aa_handle = None
#         self.log_subject = SerialLogSubject(comport, 115200)
#
#     def open(self):
#         self.log_subject.open()
#         if self.devport is not None:
#             self._aa_handle = aa_open(self.devport)
#             if self._aa_handle <= 0:
#                 raise ValueError("Unable to open Aardvark device on port %d" % self.devport)
#
#             aa_configure(self._aa_handle, AA_CONFIG_GPIO_I2C)
#             aa_target_power(self._aa_handle, 0)
#             aa_i2c_pullup(self._aa_handle, 0)
#             aa_i2c_bitrate(self._aa_handle, 400)
#             aa_i2c_bus_timeout(self._aa_handle, 150)
#
#     def close(self):
#         if self._aa_handle is not None:
#             aa_close(self._aa_handle)
#             self._aa_handle = None
#         self.log_subject.close()
#
#     def read_register(self, data_width, offset):
#         index = 0
#         w_data = array_u08(self.ADDRESS_WIDTH >> 3)
#
#         # offset = page_offset + register_offset
#         # if self.ADDRESS_WIDTH == 0x20:
#         #     index += 1
#         #     buffer1[index] = offset >> 0x18
#         # if self.ADDRESS_WIDTH >= 0x18:
#         #     index += 1
#         #     buffer1[index] = offset >> 0x10
#         # if self.ADDRESS_WIDTH >= 0x10:
#         #     index += 1
#         #     buffer1[index] = offset >> 0x08
#         index += 1
#         w_data[index] = offset     # FIXME
#         aa_i2c_write(self._aa_handle, self.DEVICE_ID >> 1, AA_I2C_NO_STOP, w_data)
#
#         r_data = array_u08(data_width >> 3)
#         aa_i2c_read(self._aa_handle, self.DEVICE_ID >> 1, AA_I2C_NO_FLAGS, r_data)
#
#         num = 0
#         for i in range(data_width >> 3):
#             num |= r_data[i] << (i << 3)
#         return num
#
#     def write_register(self, data_width, offset, data):
#         index = 0
#         num = data_width >> 3
#         w_data = array_u08(self.ADDRESS_WIDTH >> 3 + num)
#         w_data[index+1] = offset      # FIXME
#
#         for i in range(num):
#             index += 1
#             w_data[index] = data >> (i << 3)
#
#         aa_i2c_write(self._aa_handle, self.DEVICE_ID >> 1, AA_I2C_NO_FLAGS, w_data)

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)-15s - %(thread)-5d [%(levelname)-8s] - %(message)s',
    )

    # serial log enable: 0x98: 00410DA5
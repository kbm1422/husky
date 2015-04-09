import logging

logger = logging.getLogger(__name__)

from simg.test.framework import TestCase
import time


class BaseTestCase(TestCase):
    def make_scan(self, duration, interval, uevent_listen_timeout, reset_mode=False):
        assert duration >= 0, "No negative number for duration is allowed"
        assert interval >= 0, "No negative number for interval is allowed"
        assert uevent_listen_timeout >= 0, "No negative number for event listener timeout is allowed"
        with self.txunit.device.uevent.listen("wvan_scan_started") as listener, self.txunit.device.uevent.listen(
                "wvan_scan_complete") as listener2, self.txunit.device.uevent.listen("wvan_scan_stopped") as listener3:
            if reset_mode or self.txunit.device.getMode() != "wihd":
                self.txunit.device.resetMode()

            start = time.time()
            self.txunit.device.scan(duration, interval)

            # Make sure the start event is captured
            start_event = listener.get(timeout=uevent_listen_timeout)
            self.assertIsNotNone(start_event, "should get uevent 'wvan_scan_started' in %ds" % uevent_listen_timeout)

            # once_done flag is to make sure the self.assertIn only be verified once during polling the listener2's
            # content
            once_done = False
            while True:
                complete_event = listener2.get(block=False)
                if not complete_event:
                    if not once_done:
                        state = self.txunit.device.getDevState()
                        self.assertIn("scan", state, "current state should be 'scan'")
                        once_done = True
                else:
                    end = time.time()
                    if not duration < 5:
                        self.assertLessEqual(end - start, duration,
                                             "The total elapsed time is %d which should be less or equal than the "
                                             "duration %d" % (end - start, duration))
                    break
                # Sleep to prevent large duplicate log is printed out
                time.sleep(0.5)

            """duration > 0 means that:
                - period scan
                - continuous scan
            The stop event will be triggered for these type of scans
            """
            if duration > 0:
                stop_event = listener3.get(timeout=uevent_listen_timeout + duration)
                self.assertIsNotNone(stop_event, "The scan stop event should be captured")

            """duration == 0 means that:
                - one shot scan
                - continuous scan with unlimited duration
            so we sleep 10s to wait at least scan once and will capture complete event at least once.
            """
            if duration == 0:
                time.sleep(10)
                # interval == 0 means it is one shot scan
                if interval == 0:
                    self.assertEqual(listener2.queue.qsize(), 0, "No more complete event for one shot scan")
                else:
                    self.assertGreaterEqual(listener2.queue.qsize(), 1, "At least one complete scan after sleep 10s")
            # one general scan in current panda board is 4.8s, we measure the repeated scan times based on this number
            # if duration < 5, there is only one scan which is already taken above code
            elif duration < 5:
                self.assertEqual(listener2.queue.qsize(), 0, "No more complete event for the duration less than 5")
            # if duration > 5, there will at least one more scan after sleep the script 10s
            else:
                # if interval == 0, the scan frequency will be based on the actual running time until the duration
                # experies
                if interval == 0:
                    self.assertGreaterEqual(listener2.queue.qsize(), 1, "At least one complete scan after sleep 10s")
                else:
                    total_repeat_times = int(duration / interval)
                    self.assertEqual(listener2.queue.qsize() + 1, total_repeat_times,
                                     "The repeated times should be equal to the duration / interval")

    def make_interval_scan(self, uevent_listen_timeout=10):
        self.make_scan(30, 5, uevent_listen_timeout)

    def make_concurrent_scan(self, txunit, scaners=2):
        results = dict()
        with self.txunit.device.uevent.listen("wvan_scan_started") as listener:
            for _ in range(scaners):
                resp = txunit.device.scan(0, 0)
                self.assertEqual(resp, "1", "cat scan value should be 1", iswarning=True)

                state = self.txunit.device.getDevState()
                self.assertIn("scan", state, "current state should be 'scan'")

                time.sleep(2)

    def make_stop_scan(self, txunit):
        with self.txunit.device.uevent.listen("wvan_scan_stopped") as listener:
            txunit.device.stop_scan()

            with self.txunit.device.uevent.listen("wvan_scan_complete") as listener2:
                self.assertIsNone(listener2.get(timeout=15))

            time.sleep(5)

            self.assertIsNotNone(listener.get(timeout=15))

    def make_no_scan(self, txunit):
        txunit.device.stop_scan()

    def make_associated(self, txunit, rxunit):
        if txunit.device.getMode() != "wihd":
            self.make_mode(txunit, "wihd")
        elif self.txunit.device.getDevState() == "associated":
            return
        wvans = self._test_scan(txunit, rxunit)
        self._test_join(txunit, [wvans[0]["id"], wvans[0]["hr"], wvans[0]["lr"]])

    def make_associated_from_intervalscan(self, txunit, rxunit, duration, interval):
        if txunit.device.getMode() != "wihd":
            self.make_mode(txunit, "wihd")

        if interval == 0:
            self._fail("Interval should not be 0 for repeated scans")
            return

        repeat_times = int(duration / interval) + 1
        wvans = None

        for _ in range(repeat_times):
            wvans = self._test_scan(txunit, rxunit)
        self._test_join(txunit, [wvans[0]["id"], wvans[0]["hr"], wvans[0]["lr"]])

    def make_disassociated(self, txunit):
        if txunit.device.catJoin() == [0, 0, 0] and "idle" in txunit.device.getDevState():
            pass
        else:
            with txunit.device.uevent.listen("disassociated") as listener:
                expect = [0, 0, 0]
                txunit.device.join(expect)
                time.sleep(0.5)
                actual = txunit.device.catJoin()
                self.assertSequenceEqual(actual, expect, "join value should be %s" % expect)

                state = txunit.device.getDevState()
                self.assertIn("idle", state, "current state should be 'idle'")

                event = listener.get(timeout=3.0)
                self.assertIsNotNone(event, "should get uevent 'disassociated' in 3s")

    def try_disassociated(self, txunit, max_times=3):
        while True:
            count = 0
            try:
                self.make_disassociated(txunit)
                break
            except AssertionError:
                if count < max_times:
                    time.sleep(2)
                    count += 1
                else:
                    self._fail("Driver state cannot be set in idle mode, test exit")
                    raise

    def make_connected(self, txunit, rxunit, mode=1):
        if "connected" != txunit.device.getDevState():
            self.make_associated(txunit, rxunit)
            if mode == 2:
                rxmac = 1
            else:
                rxmac = rxunit.device.getMacAddress()
            self._test_connect(txunit, rxmac)

    def make_disconnected(self, txunit, rxunit):
        if "connected" == txunit.device.getDevState():
            self._test_disconnect(txunit)

    def make_mode(self, unit, expect):
        logger.debug("make sure mode is %s" % expect)
        actual = unit.device.getMode()
        if actual != expect:
            self._test_mode(unit, expect)

    def _test_mode(self, unit, mode, timeout=2.0):
        with unit.device.uevent.listen("mode_change") as listener:
            unit.device.setMode(mode)
            event = listener.get(timeout=timeout)
            self.assertEqual(event.data, mode,
                             "should get uevent 'mode_change' and its data should be '%s' in 2s" % mode)

    def _test_scan(self, txunit, rxunit):
        with txunit.device.uevent.listen("wvan_scan_complete") as listener:
            """{"event":"wvan_scan_complete","data":[{"name":"123","id":127,"hr":2,"lr":2,"strength":77}]}"""
            resp = txunit.device.scan()
            # self.assertEqual(resp, "1", "cat scan value should be 1", iswarning=True)

            state = txunit.device.getDevState()
            self.assertIn("scan", state, "current state should be 'scan'")

            event = listener.get(timeout=5.0)

            self.assertIsNotNone(event, "should get uevent 'wvan_scan_complete' in 5s")
            return event.data

    def _test_join(self, txunit, wvan):
        with txunit.device.uevent.listen("associated") as listener:
            txunit.device.join(wvan)
            event = listener.get(timeout=15)
            self.assertIsNotNone(event, "should get uevent 'associated' in 15s")

            actual = txunit.device.catJoin()
            self.assertListEqual(actual, wvan, "cat 'wihd/wvan/join' to check joined wvan")

            resp = txunit.device.getDevState()
            self.assertIn("associated", resp, "check associated, cat 'wihd/state' response should be associated")

    def _test_connect(self, txunit, rxmac):
        with txunit.device.uevent.listen("av_enabled") as listener:
            txunit.device.connect(rxmac)
            event = listener.get(timeout=15)

            self.assertIsNotNone(event, "should get uevent 'av_enabled' in 15s")

            resp = txunit.device.getDevState()
            self.assertIn("av_enabled", resp, "check av_enabled, cat 'wihd/state' response should be av_enabled")
        time.sleep(10)

    def _test_disconnect(self, txunit):
        with txunit.device.uevent.listen("disconnected") as listener:
            txunit.device.disconnect()
            self.assertEqual(0, txunit.device.catConnect(), "The current connect value should be 0")
            self.assertEqual("idle", txunit.device.getDevState(), "The device status should be idle")
            events = listener.get(timeout=5)
            self.assertIsNotNone(events.data, "The disconnected message should be captured")

    def _test_search(self, txunit):
        old_state = txunit.device.getDevState()
        with txunit.device.uevent.listen("dev_search_complete") as listener:
            txunit.device.search()
            new_state = txunit.device.getDevState()
            self.assertEqual(old_state, new_state, "driver state should be changed during searching")


if __name__ == "__main__":
    pass

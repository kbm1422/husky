import logging
logger = logging.getLogger(__name__)

from .base import BaseTestCase
from simg.test.framework import TestContextManager


class SearchFromAssociatedTestCase(BaseTestCase):
    @classmethod
    def setUpClass(cls):
        txunit, rxunit = TestContextManager.getCurrentContext().resource.acquire_pair()
        basecase = BaseTestCase()
        basecase.make_disassociated(txunit)
        basecase.make_associated(txunit, rxunit)

    def test__search_from_associated(self):
        self.txunit, self.rxunit = TestContextManager.getCurrentContext().resource.acquire_pair()
        self._test_search(self.txunit)

    @classmethod
    def tearDownClass(cls):
        txunit, rxunit = TestContextManager.getCurrentContext().resource.acquire_pair()
        BaseTestCase()._test_connect(txunit, rxunit.device.getMacAddress())


class SearchFromConnectedTestCase(BaseTestCase):
    @classmethod
    def setUpClass(cls):
        txunit, rxunit = TestContextManager.getCurrentContext().resource.acquire_pair()
        basecase = BaseTestCase()
        basecase.make_disassociated(txunit)
        basecase.make_connected(txunit, rxunit)

    def test__search_from_connected(self):
        txunit, rxunit = TestContextManager.getCurrentContext().resource.acquire_pair()
        self.make_connected(txunit, rxunit)
        self._test_search(txunit)


class SearchFromConnectAndDisconnectTestCase(BaseTestCase):
    @classmethod
    def setUpClass(cls):
        txunit, rxunit = TestContextManager.getCurrentContext().resource.acquire_pair()
        basecase = BaseTestCase()
        basecase.make_disassociated(txunit)
        basecase.make_connected(txunit, rxunit)

    def test__search_between_connect_disconnect(self):
        txunit, rxunit = TestContextManager.getCurrentContext().resource.acquire_pair()
        self.make_connected(txunit, rxunit)
        self._test_search(txunit)
        self._test_disconnect(self.txunit)
        self._test_search(txunit)

    @classmethod
    def tearDownClass(cls):
        txunit, rxunit = TestContextManager.getCurrentContext().resource.acquire_pair()
        BaseTestCase().make_connected(txunit, rxunit)

__test_suite__ = {
    "name": "BA Driver Mode Change Test Suite",
    "subs": [
        SearchFromAssociatedTestCase.test__search_from_associated,
        SearchFromConnectedTestCase.test__search_from_connected,
        SearchFromConnectAndDisconnectTestCase.test__search_between_connect_disconnect,
        ]
}
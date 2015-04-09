
import logging
from simg.test.framework import LinkedTestCase, TestCase, parametrize, name


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)-15s %(thread)-5d [%(levelname)-8s] - %(message)s'
    )

    @parametrize("base1")
    class Base1(TestCase):
        pass

    # @parametrize("base2")
    # class Base2(TestCase):
    #     pass
    #
    # @parametrize("attr1")
    # @parametrize("attr2")
    # @parametrize("attr3")
    # @parametrize("base1", type=int)
    # @parametrize("base2", type=int)
    # class Test(Base1, Base2):
    #     @parametrize("attr4")
    #     def test_func(self):
    #         self.assertEquals(self.base1, self.base2)
    #
    # class LinkedTest(LinkedTestCase):
    #     @name("2222222")
    #     def test1(self):
    #         pass

    # test1 = Test("test_func")
    # test1.run()
    # print test1._get_parametrize_marks()
    # print test1.name
#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger(__name__)

import inspect
from collections import OrderedDict


def _marked_on_class_or_func(*args, **kwargs):
    if args and not kwargs and len(args) == 1 and (inspect.isfunction(args[0]) or inspect.isclass(args[0])):
        return True
    return False


class Inject(object):
    MARK_NAME = "__simg_test_inject__"


class NameDecorator(object):
    MARK_NAME = "__simg_test_name__"

    def __init__(self, name=None):
        self.name = name

    def __call__(self, *args, **kwargs):
        if _marked_on_class_or_func(*args, **kwargs):
            item = args[0]
            setattr(item, self.MARK_NAME, self)
            return item
        else:
            return self.__class__(*args, **kwargs)


class ParametrizeDecorator(object):
    """
    The default @parametrize is a instance of ParametrizeDecorator, which has already defined in this module(mark.py)
    @param attrname: attribute name
    @param type: Specify the type of attribute value, default is str.
                 If the value is not match with the type, it will be converted.
    @param default: specify the default attribute value

    Sample:
    parametrize = ParametrizeDecorator()
    @parametrize("attr1", type=int, default=1)
    class Test(TestCase):
        @parametrize("attr2", type=int, default="1")
        def test_func(self):
            self.assertEquals(self.attr1, self.attr2, msg="%s %s" % (1, 1))
    """
    MARK_NAME = "__simg_test_parametrize__"

    class FetchType(object):
        EAGER = 1
        LAZY = 2

    class FetchContext(object):
        def __init__(self, type, globals=None, locals=None):
            self.type = type
            self.globals = globals
            self.locals = locals

            #if type is LAZY, get globals and locals of the frame which the decorator marked on.
            if self.type == ParametrizeDecorator.FetchType.LAZY:
                frame = inspect.currentframe()
                outer_frames = inspect.getouterframes(frame)
                if self.globals is None:
                    self.globals = outer_frames[3][0].f_globals
                if self.locals is None:
                    self.locals = outer_frames[3][0].f_locals

    def __init__(self, name=None, type=str, default=None, fetch=FetchType.EAGER, choice=None, iteration=None,
                 description=None):
        self.name = name
        self.type = type
        self.default = default
        self.context = self.FetchContext(fetch)
        self.choice = choice or ()
        self.iteration = iteration
        self.description = description

    def __call__(self, *args, **kwargs):
        if _marked_on_class_or_func(*args, **kwargs):
            item = args[0]

            if not hasattr(item, self.MARK_NAME):
                setattr(item, self.MARK_NAME, OrderedDict())
            else:
                # If the item is a class and it has attribute __simg_test_parametrize__, there are two possibilities:
                #   1) it is inherited from base class
                #   2) there are multiple @parametrize marked on this class, it is created by previous @parametrize
                # Current solution:
                #   For each time when @parametrize mark on this class, create a new OrderedDict() to save all marks.
                if inspect.isclass(item):
                    old_marks = getattr(item, self.MARK_NAME)
                    new_marks = OrderedDict()
                    for base_class in item.__bases__:
                        if hasattr(base_class, self.MARK_NAME):
                            new_marks.update(getattr(base_class, self.MARK_NAME).copy())
                    new_marks.update(old_marks.copy())
                    setattr(item, self.MARK_NAME, new_marks)

            marks = getattr(item, self.MARK_NAME)
            marks[self.name] = self
            return item
        else:
            return self.__class__(*args, **kwargs)

    def __repr__(self):
        return "<ParametrizeDecorator attrname: %s, type:%s, default:%s>" % (self.name, self.type, self.default)

    def __str__(self):
        return self.__repr__()


class SkipIfDecorator(object):
    """
    The default @skipif is a instance of SkipIfDecorator, which has already defined in this module(mark.py)
    @param condition: can be a function, lambda, bool or string(eval)
    @param reason: specify the skip reason

    The @skipif condition will be evaluated when case run, see method TestCase.run for detail in case.py

    Sample:
        @skipif(lambda: var1 != var2, "test class")
        class Test(TestCase):
            @skipif("1==2", "test func")
            def test_func(self):
                self.assertEquals(1, 1, msg="%s %s" % (1, 1))
    """
    MARK_NAME = "__simg_test_skipif__"

    def __init__(self, condition=None, reason=None):
        self.condition = condition
        self.reason = reason

    def __call__(self, *args, **kwargs):
        """
        If there is only a single argument and it is a function or class, set self as an addtional attribute on it.
        Otherwise, create a new decorator instance with condition and reason

        So, when decorate on the function or class:
        1. It will create new decorator instance firstly.
        2. And then it will set it self as a attribute of test_func

        Sample:
        skipif = SkipIfDecorator()
        @skipif("1==2", "test func")
        def test_func(self):
            pass

        print test_func.__simg_test_skipif__
        """
        if _marked_on_class_or_func(*args, **kwargs):
            item = args[0]
            setattr(item, self.MARK_NAME, self)
            return item
        else:
            return self.__class__(*args, **kwargs)

    def __repr__(self):
        return "<SkipIfDecorator condition: %s, reason: %s>" % (self.condition, self.reason)

    def __str__(self):
        return self.__repr__()


name = NameDecorator()
parametrize = ParametrizeDecorator()
skipif = SkipIfDecorator()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)-15s %(thread)-5d [%(levelname)-8s] - %(message)s'
    )
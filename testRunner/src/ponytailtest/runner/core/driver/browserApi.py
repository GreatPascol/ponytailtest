# -*- coding: utf-8 -*-
from ponytailtest.common.exception import *


class BrowserApi(object):
    """
    click, double click, click_first_row_of_table
    input,
    select,
    screen shot,
    assert

    other:
    """
    def __init__(self, driver):
        self._driver = driver
        self.screen_shot_imgs = {}
        self.current_test_id = ""

    @property
    def driver(self, xpath):
        return self._driver

    def raise_not_implemented_exception(self, xpath):
        raise TesterException("not supported api method in %s" % self.__class__.__name__)

    def click(self, xpath):
        self.raise_not_implemented_exception()

    def double_click(self, xpath):
        self.raise_not_implemented_exception()

    def click_first_row_of_table(self, xpath):
        self.raise_not_implemented_exception()

    def input(self, xpath):
        self.raise_not_implemented_exception()

    def select(self, xpath):
        self.raise_not_implemented_exception()

    def click(self, xpath):
        self.raise_not_implemented_exception()

    def click(self, xpath):
        self.raise_not_implemented_exception()

    def click(self, xpath):
        self.raise_not_implemented_exception()



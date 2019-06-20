# -*- coding: utf-8 -*-
import time
import traceback
from ponytailtest.core.driver.browserApi import BrowserApi
from ponytailtest.common.exception import *


def format_traceback(msg):
    return msg + ", error info: \n%s" % traceback.format_exc()


class GeneralBrowserApi(BrowserApi):

    def get_imgs(self, case_num):
        if case_num in self.screen_shot_imgs:
            return self.screen_shot_imgs[case_num]
        else:
            return []

    def _screen_shot(self, case_num):
        filename = "%s_%s.png" % (case_num, time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime(time.time())))
        img_root = runningConstants.IMG_PATH
        f_path = "%s/%s" % (img_root, filename)
        self._webdriver.get_screenshot_as_file(f_path)
        if case_num in self.screen_shot_imgs:
            self.screen_shot_imgs[case_num].append(filename)
        else:
            self.screen_shot_imgs[case_num] = [filename]

    def click(self, xpath):
        element = self._find(xpath)
        try:
            element.click()
        except Exception as e:
            raise ElementClickException(format_traceback("Element can not be clicked('%s')" % xpath))

    def double_click(self, xpath):
        element = self._find(xpath)
        try:
            webdriverUtil.double_click(self._webdriver, element)
        except Exception as e:
            raise ElementClickException(format_traceback("Element can not be clicked('%s')" % xpath))

    def _input(self, xpath, value):
        element = self._find(xpath)
        try:
            self._webdriver.execute_script("arguments[0].scrollIntoView(true);", element)
            element.send_keys(value)
        except Exception as e:
            raise ElementClickException("Element can not click(%s).")

    # def _clear(self, xpath):
    #     element = self._find(xpath)
    #     try:
    #         webdriverUtil.clear_element(self._webdriver, element)
    #     except Exception as e:
    #         raise ElementClearException("Element can not clear(%s).")

    def _select(self, xpath, text):
        element = self._find(xpath)
        webdriverUtil.select_option_by_text(element, text)

    def _find(self, xpath, timeout=30):
        try:
            return webdriverUtil.find_element_with_wait_clickable(self._webdriver, xpath, timeout)
        except Exception as e:
            raise ScriptException(format_traceback("Element not found or clickable: xpath(%s)" % xpath))

    ###################################################
    # switch to frame or window

    def _switch_to_frame(self, xpath):
        self._webdriver.switch_to.frame(self._find(xpath, 30))

    def _switch_back(self):
        self._webdriver.switch_to.parent_frame()

    def _switch_to_default(self):
        self._webdriver.switch_to.default_content()

    def _switch_to_popup_window(self):
        self._webdriver.switch_to.window(self._webdriver.window_handles[1])

    ###################################################
    # wait and exists

    @staticmethod
    def _wait(timeout):
        """ 死板的wait """
        time.sleep(timeout)

    def _wait_till_exist(self, xpath, timeout=30):
        """ 一直wait到found直到timeout """
        return webdriverUtil.find_element_with_wait_presence(self._webdriver, xpath, timeout)

    def _exist(self, xpath: object) -> object:
        return len(webdriverUtil.find_element_list(self._webdriver, xpath)) > 0

    def _exist_with_wait(self, xpath, timeout=30):
        return webdriverUtil.find_element_with_wait_presence(self._webdriver, xpath, timeout) is not None

    ######################################
    # assert

    def _assert_text(self, xpath, text, msg=None):
        element_text = self._find(xpath).text
        if msg is None:
            msg = "Assert not equal:  element.text = '%s' by xpath(%s)" % (element_text, xpath)
        self.assertEqual(element_text.strip(), text.strip(), msg)

    def _assert_exist(self, xpath, msg=None):
        if msg is None:
            msg = "Assert error: element(%s) not exist" % xpath
        self.assertTrue(self._exist(xpath), msg)

    def _assert_not_exist(self, xpath, msg=None):
        if msg is None:
            msg = "Assert error: element(%s) exist" % xpath
        self.assertFalse(self._exist(xpath), msg)

    def _assert_in_table_col(self, table_xpath, text, column, msg=None):
        webdriverUtil.wait_table_data(xpath=table_xpath)
        cells = self._webdriver.find_elements_by_xpath('%s//tr//td[%d]' % (table_xpath, column))
        texts_got = []
        for e in cells:
            t = self._webdriver.execute_script("return arguments[0].innerText;", e).strip()
            texts_got.append(t)
            if t == text:
                return
        if msg is None:
            msg = "Assert not exist: '%s' not in table('%s'), col(%d): %s" % (text, table_xpath, column, str(texts_got))
        self.assertTrue(False, msg)

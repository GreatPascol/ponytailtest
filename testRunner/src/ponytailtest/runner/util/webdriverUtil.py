# -*- coding: utf-8 -*-
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import *
import src.util.stringUtil as stringUtil


webdriver_wait_ignore_exceptions = [StaleElementReferenceException, ElementNotInteractableException]


def send_request(webdriver, http_method, url):
    if url == "":
        return
    js = "xmlhttp=new XMLHttpRequest();xmlhttp.open('%s','%s',true);xmlhttp.send();" % (http_method, url)
    webdriver.execute_script(js)


def find_element(webdriver, xpath):
    return webdriver.find_element_by_xpath(xpath)


def find_element_list(webdriver, xpath):
    return webdriver.find_elements_by_xpath(xpath)


def find_element_with_wait_presence(webdriver, xpath, timeout):
    end_time = time.time() + timeout
    while True:
        try:
            return webdriver.find_element_by_xpath(xpath)
        except NoSuchElementException as exc:
            pass
        time.sleep(0.5)
        if time.time() > end_time:
            break
    return None


def find_element_with_wait_clickable(webdriver, xpath, timeout):
    webdriver_wait = WebDriverWait(webdriver, timeout, ignored_exceptions=webdriver_wait_ignore_exceptions)
    return webdriver_wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))


def wait_table_data(webdriver, xpath, timeout=75):
    end_time = time.time() + timeout
    while True:
        try:
            e_tr = webdriver.find_element_by_xpath("%s//tr" % xpath)
            if not stringUtil.is_blank(webdriver.execute_script("return arguments[0].innerText;", e_tr)):
                return
        except Exception as exc:
            pass
        time.sleep(0.5)
        if time.time() > end_time:
            break


def click_element(webdriver, element):
    """ execute js by dom scrollIntoView then click
        如果调用 webdriver.find_element_by_xpath(xx).click() 报错（e.g. not clickable, interactable)
        则可改为调用此方法，webdriver.click_element( webdriver.find_element_by_xpath(xx) )
    """
    webdriver.execute_script("arguments[0].scrollIntoView(true);arguments[0].click();", element)


def clear_element(webdriver, element):
    webdriver.execute_script("arguments[0].scrollIntoView(true);arguments[0].clear();",element)


def set_element_value(webdriver, element, value):
    """ execute js by dom value
        同click_element, 如果send_keys()报错
    """
    webdriver.execute_script("arguments[0].value = arguments[1];", element, value)


def select_option_by_text(element, text):
    Select(element).select_by_visible_text(text)


def double_click(webdriver, element):
    ActionChains(webdriver).double_click(element).perform()

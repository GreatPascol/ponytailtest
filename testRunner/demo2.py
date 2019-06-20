from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import *
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import time
from selenium.webdriver.ie.options import Options
opt = Options()
opt.native_events = True
opt.require_window_focus = True
opt.persistent_hover = False
opt.ignore_zoom_level = True
cap = {}
cap["pageLoadStrategy"] = "none"
d = webdriver.Ie(executable_path="F:/Download/chrome/IEDriverServer_x64_3.141.0/IEDriverServer.exe", capabilities=cap, options=opt, log_level="DEBUG", log_file="G:/tmp/iedriverserver.log")  # Internet Explorer浏览器
d.maximize_window()


def find(xpath, click=False):
    ct = 30
    while ct > 0:
        ct -= 1
        try:
            x = d.find_element_by_xpath(xpath)
            time.sleep(1)
            return x
        except Exception as e:
            print("finding %s" % xpath)
            time.sleep(0.15)
    return None


d.get("http://10.201.39.187:7001/mobilesg/entergd.action")
e = find("//input[@name='username']")
e.send_keys("dgadmin")
e = find("//input[@name='password']")
e.send_keys("sg123!@#")
e = find('//*[@id="tabs1"]/table/tbody/tr[2]/td/table/tbody/tr[1]/td/table/tbody/tr[4]/td[2]/input', True)
e.click()
time.sleep(1)

d.get("http://10.201.39.187:7001/mobilesg/toOSSOAction.action")

time.sleep(3)
d.switch_to.frame(find("//frame[@name='mainFrame']"))
d.switch_to.frame(find("//frame[@name='leftFrame']"))
find("//div[@id='dd0']/div/a[normalize-space(text())='待办工单']", True).click()
find("//a[@id='sd2'][normalize-space(text())='待办工单']", True).click()

d.switch_to.parent_frame()
d.switch_to.frame(find("//frame[@name='contFrame']"))
d.switch_to.frame(find("//frame[@name='topFrame']"))

e = find("//input[@name='queryParam.crmCode']").send_keys("2759801905181023")
e = find("//input[@value='查询'][@id='btn']", True).click()

d.switch_to.parent_frame()
d.switch_to.frame(find("//frame[@name='mainFrame']"))

e = find("//div[@id='listsListContainer']/table/tbody/tr[2]/td[4]", True)
e.click()
time.sleep(5)


d.switch_to.parent_frame()
d.switch_to.frame(find("//frame[@name='infoFrame']"))

d.execute_script("window.showModalDialog = function( sURL, vArguments, sFeatures){" \
                                       + "window.popupDialog = window.open(sURL, 'ponytailOpenDialog');}")

e = find("//input[@id='_signButton'][@name='signBut']", True)
e.click()

d.switch_to.window("ponytailOpenDialog")
d.maximize_window()
d.refresh()
d.execute_script("window.close = function(){}")

find("//input[contains(@class,'button1')]", True).click()
find("//input[@id='ext-comp-1014'][@name='loginName']").send_keys("dwhuangshaofu")
find("//button[@id='ext-gen147']", True).click()
e = find("//div[contains(@class,'x-grid3-row-first')]/table/tbody/tr[1]/td[3]", True)
e.click()
find("//button[@id='ext-gen88']", True).click()
find("//button[@id='ext-gen12']", True).click()
find("//button[text()='OK']", True).click()

ret_value = d.execute_script("return window.returnValue;")
ret_value = ret_value if ret_value else ''
d.close()
d.switch_to.window(d.window_handles[0])
d.switch_to.frame(find("//frame[@name='mainFrame']"))
d.switch_to.frame(find("//frame[@name='contFrame']"))
d.switch_to.frame(find("//frame[@name='infoFrame']"))
d.execute_script("window.showModalDialog = function( sURL, vArguments, sFeatures){" \
                                       + "return '" + ret_value + "';}")

e = find("//input[@id='_signButton'][@name='signBut']", True)
e.click()

find("//input[@id='_doActionId']", True).click()
time.sleep(1)
d.switch_to.alert.accept()

d.quit()

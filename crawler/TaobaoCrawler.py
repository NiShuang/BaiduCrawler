#-*- coding: UTF-8 -*-

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import datetime
import urllib
import urllib2
import json
from PIL import Image as IMG

class TaobaoCrawler:
        def __init__(self,keyword = 'insta360+Nano'):
            cap = webdriver.DesiredCapabilities.PHANTOMJS
            cap["phantomjs.page.settings.resourceTimeout"] = 1000
            cap["phantomjs.page.settings.loadImages"] = False
            cap["phantomjs.page.settings.localToRemoteUrlAccessEnabled"] = True
            cap["userAgent"] = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0"
            cap["XSSAuditingEnabled"] = True
            self.driver = webdriver.PhantomJS(desired_capabilities=cap)
            # self.driver = webdriver.Chrome()
            self.date = time.strftime('%Y%m%d', time.localtime(time.time()))
            self. url = "https://s.taobao.com/search?q="+keyword+"&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_"+self.date+"&ie=utf8"

        def start(self):
            print 'init'
            self.driver.get(self.url)
            print 'before'
            print self.driver.page_source
            print 'after'
            wait = WebDriverWait(self.driver, 10)
            elements = wait.until(lambda x: x.find_elements_by_class_name("J_IconMoreNew"))
            for element in elements:
                print element.find_element_by_xpath("div[@class='row row-2 title']/a").text

            print self.driver.find_element_by_xpath("// *[ @ id = 'mainsrp-pager'] / div / div / div / div[1]").text

            self.driver.close()


if __name__=="__main__":
    print "aaaa"
    crawler = TaobaoCrawler('insta360+Nano')
    crawler.start()
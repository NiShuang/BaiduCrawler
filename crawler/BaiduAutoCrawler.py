#-*- coding: UTF-8 -*-
from selenium import webdriver
import urllib
import urllib2
import json
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pytesser import *
import ImageEnhance
from PIL import Image as IMG
import time
import re

class BaiduAutoCrawler:
        def __init__(self):
            self.driver = webdriver.Chrome()
            self.id = '10551064'
            self.siteId = '6856127'
            self.host = 'tongji.baidu.com'
            self.origin = 'http://tongji.baidu.com'
            self.username = 'insta360'
            self.password = '******'
            self.user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36'
            # self.cookie = 'BAIDUID=7DDC1F27CA20A3B1D0A338F23CDE09A8:FG=1; BIDUPSID=7DDC1F27CA20A3B1D0A338F23CDE09A8; PSTM=1468217799; uc_login_unique=e04fb29dcc1f2664a074e7c0aa20b577;hm_usertype=0; hm_username=insta360; SIGNIN_UC=70a2711cf1d3d9b1a82d2f87d633bd8a02184729599;__cas__st__=3c71942bc3ee051b589e2605fbb6accb4e456fe993d7a5f638b21c9f8a9fff912996bf6076b49b317b46e034; __cas__id__=10551064; H_PS_PSSID=1420_20537_20416_15246_12233;  '
            # self.cookie = ' BIDUPSID=7DDC1F27CA20A3B1D0A338F23CDE09A8; PSTM=1468217799; H_PS_PSSID=1420_20537_20416_15246_12233;'
            self.cookie = ''
            self. url = 'http://tongji.baidu.com/web/'+self.id+'/ajax/post'

        def login(self):
           pass

        def start(self):
            self.driver.get('http://tongji.baidu.com/web/welcome/login')

            element = self.driver.find_element_by_class_name("login-trigger")
            element.click();

            element = self.driver.find_element_by_id("UserName")
            element.send_keys(self.username)

            element = self.driver.find_element_by_id("Password")
            element.send_keys(self.password)

            valicode = self.getValicode()



            element = self.driver.find_element_by_id("Valicode")
            print 'Try valicode...'
            # input = raw_input('Pleasr input valicode:')
            element.send_keys(valicode)

            element = self.driver.find_element_by_id("Submit")
            # element.click();

            while(not self.isLogin()):
                element = self.driver.find_element_by_id("Password")
                element.send_keys(self.password)
                valicode = self.getValicode()

                element = self.driver.find_element_by_id("Valicode")
                print 'Try valicode...'
                element.send_keys(valicode)
                element = self.driver.find_element_by_id("Submit")
            # element.click();
            # wait = WebDriverWait(self.driver, 1)
            # element = wait.until(EC.element_to_by_id((By.ID, 'ErrorTip')))
            # wait = WebDriverWait(self.driver, 20)  #second
            # element = wait.until(EC.presence_of_element_located(
            #     (By.ID, 'ErrorTip')))
            # element.click();




            wait = WebDriverWait(self.driver, 100)  #second
            element = wait.until(EC.presence_of_element_located(
                (By.XPATH, '//a[@href="/web/10551064/trend/time?siteId='+self.siteId+'&flag=month"]')))
            element.click();

            cookies = self.driver.get_cookies()
            print cookies
            for cookie in cookies:
                print cookie['name']+' : '+cookie['value']
                self.cookie = self.cookie + cookie['name'] + '=' + cookie['value'] + ';'
                # self.driver.close()
            self.getTrendByDay(clientDevice = 'pc');
            print
            self.getTrendByPeriod(clientDevice = 'pc');

        def getTrendByDay(self,startDate = '1465833600000',endDate = '1468339200000',clientDevice = 'all'):
            headers = {}
            headers['User-Agent'] = self.user_agent
            headers['Referer'] = 'http://tongji.baidu.com/web/'+self.id+'/trend/time?siteId='+self.siteId+'&flag=month'
            headers['Cookie'] = self.cookie
            headers['Host'] = self.host
            headers['Origin'] = self.origin
            headers['X-Requested-With'] = 'XMLHttpRequest'
            headers['Content-Type'] = 'application/x-www-form-urlencoded'
            headers['Connection'] = 'keep-alive'

            data = {}
            data['siteId'] = self.siteId
            data['clientDevice'] = clientDevice
            data['st'] = startDate
            data['et'] = endDate
            data['st2'] = '0'
            data['et2'] = '0'
            data['indicators'] = 'pv_count,visitor_count,ip_count,bounce_ratio,avg_visit_time,visit_count'
            data['order'] = 'simple_date_title,desc'
            data['offset'] = '0'
            data['pageSize'] = '9999999'
            data['gran'] = '5'
            data['flag'] = 'month'
            data['reportId'] = '3'
            data['method'] = 'trend/time/a'
            data['queryId'] = ''

            request = urllib2.Request(self.url, urllib.urlencode(data), headers=headers)
            try:
                response = urllib2.urlopen(request)
                jsonData = response.read()
                result = json.loads(jsonData, encoding="utf-8")
                data = result['data']
                fields = data['fields']
                for field in fields:
                    print field,
                print

                dates = data['items'][0]
                for date in dates:
                    print date[0],
                print

                records = data['items'][1]
                for record in records:
                    print record
                print

                sum = data['sum']
                print sum[0]

            except urllib2.URLError, e:
                if hasattr(e, "code"):
                    print e.code
                if hasattr(e, "reason"):
                    print e.reason



        def getTrendByPeriod(self, startDate='1465833600000', endDate='1468339200000', clientDevice = 'all'):
            headers = {}
            headers['User-Agent'] = self.user_agent
            headers['Referer'] = 'http://tongji.baidu.com/web/' + self.id + '/trend/time?siteId=' + self.siteId + '&flag=yesterday'
            headers['Cookie'] = self.cookie
            headers['Host'] = self.host
            headers['Origin'] = self.origin
            headers['X-Requested-With'] = 'XMLHttpRequest'
            headers['Content-Type'] = 'application/x-www-form-urlencoded'
            headers['Connection'] = 'keep-alive'

            data = {}
            data['siteId'] = self.siteId
            data['clientDevice'] = clientDevice
            data['st'] = startDate
            data['et'] = endDate
            data['indicators'] = 'pv_count,visitor_count,ip_count,bounce_ratio,avg_visit_time,visit_count'
            data['order'] = 'simple_date_title,desc'
            data['offset'] = '0'
            data['pageSize'] = '24'
            data['gran'] = '6'
            data['flag'] = 'yesterday'
            data['reportId'] = '3'
            data['method'] = 'trend/time/a'
            data['queryId'] = ''

            request = urllib2.Request(self.url, urllib.urlencode(data), headers=headers)
            try:
                response = urllib2.urlopen(request)
                jsonData = response.read()
                result = json.loads(jsonData, encoding="utf-8")
                data = result['data']
                fields = data['fields']
                for field in fields:
                    print field,
                print

                dates = data['items'][0]
                for date in dates:
                    print date[0],
                print

                records = data['items'][1]
                for record in records:
                    print record
                print

                sum = data['sum']
                print sum[0]
            except urllib2.URLError, e:
                if hasattr(e, "code"):
                    print e.code
                if hasattr(e, "reason"):
                    print e.reason

        def getValicode(self):
            element = self.driver.find_element_by_id("change_cas")
            element.click();
            time.sleep(0.5)
            self.driver.get_screenshot_as_file("screenshot.png")
            img = IMG.open('screenshot.png')
            width = img.size[0]
            height =  img.size[1]
            region = (int(width*0.50699677), int(height*0.52849162), int(width*0.593110872), int(height*0.57318436))
            cropImg = img.crop(region)
            cropImg.save('1.png')
            image = IMG.open('1.png')
            enhancer = ImageEnhance.Contrast(image)
            image_enhancer = enhancer.enhance(2)
            valicode = image_to_string(image_enhancer)
            if len(valicode)==0:
                return self.getValicode()
            else:
                pattern = re.compile(r'[0-9,a-z,A-Z]{4}')
                match = pattern.match(valicode)
                if match:
                    print valicode
                    return valicode
                else:
                    return self.getValicode()

        def isLogin(self):
            try:
                time.sleep(2)
                wait = WebDriverWait(self.driver, 10)
                element = wait.until(EC.presence_of_element_located(
                    (By.ID, 'ErrorTip')))
                return False
            except NoSuchElementException:
                return True
            except TimeoutException:
                return True

spider = BaiduAutoCrawler()
spider.start()
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

class BaiduCrawler:
        def __init__(self):
            cap = webdriver.DesiredCapabilities.PHANTOMJS
            cap["phantomjs.page.settings.resourceTimeout"] = 1000
            cap["phantomjs.page.settings.loadImages"] = False
            cap["phantomjs.page.settings.localToRemoteUrlAccessEnabled"] = True
            self.driver = webdriver.PhantomJS(desired_capabilities=cap,
                                          service_args=['--ignore-ssl-errors=true', '--ssl-protocol=any',
                                                        '--web-security=true'])
            self.id = '10551064' #insta360 id
            # self.siteId = '6856127' #insta360.com = 6856127 ; cloud.insta360.com = 8268996 ;  live.insta360.com = 8269014 ; help.insta360.com = 8269026 ;  nano.insta360.com = 9216773
            self.siteID = {
                'home' : '6856127',
                'cloud': '8268996',
                'live': '8269014',
                'help': '8269026',
                'nano': '9216773',
            }
            self.host = 'tongji.baidu.com'
            self.origin = 'http://tongji.baidu.com'
            self.username = 'insta360'
            self.password = '******'
            self.user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36'
            # self.cookie = 'BAIDUID=7DDC1F27CA20A3B1D0A338F23CDE09A8:FG=1; BIDUPSID=7DDC1F27CA20A3B1D0A338F23CDE09A8; PSTM=1468217799; uc_login_unique=e04fb29dcc1f2664a074e7c0aa20b577;hm_usertype=0; hm_username=insta360; SIGNIN_UC=70a2711cf1d3d9b1a82d2f87d633bd8a02184729599;__cas__st__=3c71942bc3ee051b589e2605fbb6accb4e456fe993d7a5f638b21c9f8a9fff912996bf6076b49b317b46e034; __cas__id__=10551064; H_PS_PSSID=1420_20537_20416_15246_12233;  '
            self.cookie = ''
            self. url = 'http://tongji.baidu.com/web/'+self.id+'/ajax/post'

        def start(self):
            self.driver.get('http://tongji.baidu.com/web/welcome/login')

            element = self.driver.find_element_by_class_name("login-trigger")
            element.click();

            element = self.driver.find_element_by_id("UserName")
            element.send_keys(self.username)

            element = self.driver.find_element_by_id("Password")
            element.send_keys(self.password)

            time.sleep(1)

            self.driver.get_screenshot_as_file("screenshot.png")
            img = IMG.open('screenshot.png')
            img.show()

            element = self.driver.find_element_by_id("Valicode")
            input = raw_input('Please input captcha:')
            element.send_keys(input)

            element = self.driver.find_element_by_id("Submit")
            element.click();

            while(not self.isLogin()):
                element = self.driver.find_element_by_id("Password")
                element.send_keys(self.password)

                element = self.driver.find_element_by_id("Valicode")
                input = raw_input('Please input captcha:')
                element.send_keys(input)

                element = self.driver.find_element_by_id("Submit")
                element.click()

            wait = WebDriverWait(self.driver, 100)  #second
            element = wait.until(EC.presence_of_element_located(
                (By.XPATH, '//a[@href="/web/10551064/trend/time?siteId='+self.siteID['home']+'&flag=month"]')))
            element.click()

            cookies = self.driver.get_cookies()
            print cookies
            for cookie in cookies:
                print cookie['name']+' : '+cookie['value']
                self.cookie = self.cookie + cookie['name'] + '=' + cookie['value'] + ';'
            self.driver.quit()
            # self.getTrendByDay(startDate = '2016-09-21',endDate = '2016-09-26',clientDevice = 'pc', siteID = self.siteID['home']);
            # print
            # self.getTrendByPeriod(startDate = '1465833600000',endDate = '1468339200000',clientDevice = 'pc', siteID = self.siteID['home']);
            # print
            self.getSource(date='2016-09-21',clientDevice = 'pc', siteID = self.siteID['home'])
            # print
            # self.getEngine(date=self.dateToTime('2016-07-14'), siteID = self.siteID['home'])
            # self.getLink(date=self.dateToTime('2016-07-14'), siteID=self.siteID['home'])
            self.getCountryDistribution(date = '2016-09-21', siteID = self.siteID['home'])
            # raw_input('Enter to exit')

        def getTrendByDay(self,startDate = '2016-09-21',endDate = '2016-09-26',clientDevice = 'pc', siteID = '6856127'):
            headers = {}
            headers['User-Agent'] = self.user_agent
            headers['Referer'] = 'http://tongji.baidu.com/web/'+self.id+'/trend/time?siteId='+siteID+'&flag=month'
            headers['Cookie'] = self.cookie
            headers['Host'] = self.host
            headers['Origin'] = self.origin
            headers['X-Requested-With'] = 'XMLHttpRequest'
            headers['Content-Type'] = 'application/x-www-form-urlencoded'
            headers['Connection'] = 'keep-alive'

            data = {}
            data['siteId'] = self.siteID['home']
            data['clientDevice'] = clientDevice
            data['st'] = self.dateToTime(startDate)
            data['et'] = self.dateToTime(endDate)
            data['st2'] = '0'
            data['et2'] = '0'
            data['indicators'] = 'pv_count,visitor_count,ip_count,bounce_ratio,avg_visit_time,visit_count,avg_visit_pages'
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
                jsonData = json.loads(response.read(), encoding="utf-8")
                data = jsonData['data']
                dates = data['items'][0]
                records = data['items'][1]
                result = []
                for index in range(len(dates)):
                    date = datetime.datetime.strptime(dates[index][0], '%Y/%m/%d').date().strftime('%Y-%m-%d')
                    pv_count = records[index][0]
                    visit_count = records[index][1]
                    uv_count = records[index][2]
                    ip_count = records[index][3]
                    bounce_ratio = records[index][4]
                    avg_visit_time = records[index][5]
                    avg_visit_pages = records[index][6]
                    temp = {
                        'date': date,
                        'pv_count': pv_count,
                        'visit_count': visit_count,
                        'uv_count': uv_count,
                        'ip_count': ip_count,
                        'bounce_ratio': bounce_ratio,
                        'avg_visit_time': avg_visit_time,
                        'avg_visit_pages': avg_visit_pages,
                        'clientDevice': clientDevice
                            }
                    result.append(temp)
                jsonResult = json.dumps(result)
                print jsonResult
                return jsonResult

            except urllib2.URLError, e:
                if hasattr(e, "code"):
                    print e.code
                if hasattr(e, "reason"):
                    print e.reason

        def getSource(self, date='2016-09-26', clientDevice='pc' ,siteID = '6856127'):
            headers = {}
            headers['User-Agent'] = self.user_agent
            headers['Referer'] = 'http://tongji.baidu.com/web/' + self.id + '/source/all?siteId=' + siteID
            headers['Cookie'] = self.cookie
            headers['Host'] = self.host
            headers['Origin'] = self.origin
            headers['X-Requested-With'] = 'XMLHttpRequest'
            headers['Content-Type'] = 'application/x-www-form-urlencoded'
            headers['Connection'] = 'keep-alive'

            data = {}
            data['viewType'] = 'site'
            data['siteId'] = self.siteID['home']
            data['clientDevice'] = clientDevice
            data['st'] = self.dateToTime(date)
            data['et'] = self.dateToTime(date)
            data['indicators'] = 'bounce_ratio,avg_visit_time,trans_count,trans_ratio,pv_count,visitor_count,avg_visit_pages'
            data['order'] = 'pv_count,desc'
            data['offset'] = '0'
            data['isPromotion'] = 'false'
            data['pageSize'] = '9999999'
            data['reportId'] = '9'
            data['visitor'] = 'all'
            data['method'] = 'source/all/a'
            data['queryId'] = ''

            request = urllib2.Request(self.url, urllib.urlencode(data), headers=headers)
            try:
                response = urllib2.urlopen(request)
                jsonData = json.loads(response.read(), encoding="utf-8")
                data = jsonData['data']
                result = []
                date = datetime.datetime.strptime(data['timeSpan'][0], '%Y/%m/%d').date().strftime('%Y-%m-%d')

                sources = data['items'][0]
                records = data['items'][1]
                for index in range(len(sources)):
                    site = sources[index][0]['name']
                    pv_count = records[index][0]
                    uv_count = records[index][1]
                    bounce_ratio = records[index][2]
                    avg_visit_time = records[index][3]
                    avg_visit_pages = records[index][4]
                    temp = {
                        'site': site,
                        'date': date,
                        'pv_count': pv_count,
                        'uv_count': uv_count,
                        'bounce_ratio': bounce_ratio,
                        'avg_visit_time': avg_visit_time,
                        'avg_visit_pages': avg_visit_pages,
                        'clientDevice': clientDevice
                    }
                    result.append(temp)
                jsonResult = json.dumps(result)
                print jsonResult
                return jsonResult
            except urllib2.URLError, e:
                if hasattr(e, "code"):
                    print e.code
                if hasattr(e, "reason"):
                    print e.reason

        def getCityDistribution(self, date='2016-09-26', siteID = '6856127'):
            headers = {}
            headers['User-Agent'] = self.user_agent
            headers['Referer'] = 'http://tongji.baidu.com/web/' + self.id + '/visit/district?siteId=' + siteID
            headers['Cookie'] = self.cookie
            headers['Host'] = self.host
            headers['Origin'] = self.origin
            headers['X-Requested-With'] = 'XMLHttpRequest'
            headers['Content-Type'] = 'application/x-www-form-urlencoded'
            headers['Connection'] = 'keep-alive'

            data = {}
            data['siteId'] = self.siteID['home']
            data['st'] = self.dateToTime(date)
            data['et'] = self.dateToTime(date)
            data['st2'] = '0'
            data['et2'] = '0'
            data['indicators'] = 'pv_count,visitor_count,ip_count,bounce_ratio,avg_visit_time'
            data['order'] = 'pv_count,desc'
            data['offset'] = '0'
            data['pageSize'] = '9999999'
            data['viewType'] = 'city'
            data['reportId'] = '16'
            data['method'] = 'visit/district/a'
            data['queryId'] = ''

            request = urllib2.Request(self.url, urllib.urlencode(data), headers=headers)
            try:
                response = urllib2.urlopen(request)
                jsonData = json.loads(response.read(), encoding="utf-8")
                data = jsonData['data']
                result = []
                date = datetime.datetime.strptime(data['timeSpan'][0], '%Y/%m/%d').date().strftime('%Y-%m-%d')

                sources = data['items'][0]
                records = data['items'][1]
                for index in range(len(sources)):
                    location = sources[index][0]['name']
                    pv_count = records[index][0]
                    uv_count = records[index][1]
                    ip_count = records[index][2]
                    bounce_ratio = records[index][3]
                    avg_visit_time = records[index][4]
                    temp = {
                        'location': location,
                        'date': date,
                        'pv_count': pv_count,
                        'uv_count': uv_count,
                        'ip_count': ip_count,
                        'bounce_ratio': bounce_ratio,
                        'avg_visit_time': avg_visit_time,
                        'is_city': 1
                    }
                    result.append(temp)
                jsonResult = json.dumps(result)
                print jsonResult
                return jsonResult
            except urllib2.URLError, e:
                if hasattr(e, "code"):
                    print e.code
                if hasattr(e, "reason"):
                    print e.reason

        def getCountryDistribution(self, date='2016-09-26', siteID = '6856127'):
            headers = {}
            headers['User-Agent'] = self.user_agent
            headers['Referer'] = 'http://tongji.baidu.com/web/' + self.id + '/visit/world?siteId=' + siteID
            headers['Cookie'] = self.cookie
            headers['Host'] = self.host
            headers['Origin'] = self.origin
            headers['X-Requested-With'] = 'XMLHttpRequest'
            headers['Content-Type'] = 'application/x-www-form-urlencoded'
            headers['Connection'] = 'keep-alive'

            data = {}
            data['siteId'] = self.siteID['home']
            data['st'] = self.dateToTime(date)
            data['et'] = self.dateToTime(date)
            data['st2'] = '0'
            data['et2'] = '0'
            data['indicators'] = 'pv_count,visitor_count,ip_count,bounce_ratio,avg_visit_time'
            data['order'] = 'pv_count,desc'
            data['offset'] = '0'
            data['pageSize'] = '9999999'
            data['reportId'] = '42'
            data['method'] = 'visit/world/a'
            data['queryId'] = ''

            request = urllib2.Request(self.url, urllib.urlencode(data), headers=headers)
            try:
                response = urllib2.urlopen(request)
                jsonData = json.loads(response.read(), encoding="utf-8")
                data = jsonData['data']
                result = []
                date = datetime.datetime.strptime(data['timeSpan'][0], '%Y/%m/%d').date().strftime('%Y-%m-%d')

                sources = data['items'][0]
                records = data['items'][1]
                for index in range(len(sources)):
                    location = sources[index][0]['name']
                    pv_count = records[index][0]
                    uv_count = records[index][1]
                    ip_count = records[index][2]
                    bounce_ratio = records[index][3]
                    avg_visit_time = records[index][4]
                    temp = {
                        'location': location,
                        'date': date,
                        'pv_count': pv_count,
                        'uv_count': uv_count,
                        'ip_count': ip_count,
                        'bounce_ratio': bounce_ratio,
                        'avg_visit_time': avg_visit_time,
                        'is_city': 0
                    }
                    result.append(temp)
                jsonResult = json.dumps(result)
                print jsonResult
                return jsonResult
            except urllib2.URLError, e:
                if hasattr(e, "code"):
                    print e.code
                if hasattr(e, "reason"):
                    print e.reason

        def getEngine(self, date='2016-09-26', clientDevice='all' ,siteID = '6856127'):
            headers = {}
            headers['User-Agent'] = self.user_agent
            headers['Referer'] = 'http://tongji.baidu.com/web/' + self.id + '/source/engine?siteId=' + siteID
            headers['Cookie'] = self.cookie
            headers['Host'] = self.host
            headers['Origin'] = self.origin
            headers['X-Requested-With'] = 'XMLHttpRequest'
            headers['Content-Type'] = 'application/x-www-form-urlencoded'
            headers['Connection'] = 'keep-alive'

            data = {}
            data['siteId'] = self.siteID['home']
            data['area'] = 'all'
            data['visitor'] = 'all'
            data['clientDevice'] = clientDevice
            data['st'] = self.dateToTime(date)
            data['et'] = self.dateToTime(date)
            data['st2'] = '0'
            data['et2'] = '0'
            data['indicators'] = 'pv_count,visitor_count,ip_count,bounce_ratio,avg_visit_time'
            data['order'] = 'pv_count,desc'
            data['isPromotion'] = 'false'
            data['reportId'] = '10'
            data['pageSize'] = '9999999'
            data['method'] = 'source/engine/a'
            data['queryId'] = ''

            request = urllib2.Request(self.url, urllib.urlencode(data), headers=headers)
            try:
                response = urllib2.urlopen(request)
                jsonData = response.read()
                print jsonData
                result = json.loads(jsonData, encoding="utf-8")
            except urllib2.URLError, e:
                if hasattr(e, "code"):
                    print e.code
                if hasattr(e, "reason"):
                    print e.reason

        def getLink(self, date='2016-09-26', clientDevice='all' ,siteID = '6856127'):
            headers = {}
            headers['User-Agent'] = self.user_agent
            headers['Referer'] = 'http://tongji.baidu.com/web/' + self.id + '/source/link?siteId=' + siteID
            headers['Cookie'] = self.cookie
            headers['Host'] = self.host
            headers['Origin'] = self.origin
            headers['X-Requested-With'] = 'XMLHttpRequest'
            headers['Content-Type'] = 'application/x-www-form-urlencoded'
            headers['Connection'] = 'keep-alive'

            data = {}
            data['viewType'] = 'domain'
            data['siteId'] = self.siteID['home']
            data['visitor'] = 'all'
            data['clientDevice'] = clientDevice
            data['st'] = self.dateToTime(date)
            data['et'] = self.dateToTime(date)
            data['st2'] = ''
            data['et2'] = ''
            data['indicators'] = 'pv_count,visitor_count,ip_count,bounce_ratio,avg_visit_time'
            data['order'] = 'pv_count,desc'
            data['offset'] = '0'
            data['reportId'] = '13'
            data['domainType'] = '0'
            data['pageSize'] = '9999999'
            data['method'] = 'source/link/a'
            data['queryId'] = ''

            request = urllib2.Request(self.url, urllib.urlencode(data), headers=headers)
            try:
                response = urllib2.urlopen(request)
                jsonData = response.read()
                print jsonData
                result = json.loads(jsonData, encoding="utf-8")
            except urllib2.URLError, e:
                if hasattr(e, "code"):
                    print e.code
                if hasattr(e, "reason"):
                    print e.reason

        def getTrendByPeriod(self, startDate='2016-09-16', endDate='2016-09-26', clientDevice = 'all', siteID = '6856127'):
            headers = {}
            headers['User-Agent'] = self.user_agent
            headers['Referer'] = 'http://tongji.baidu.com/web/' + self.id + '/trend/time?siteId=' + siteID + '&flag=yesterday'
            headers['Cookie'] = self.cookie
            headers['Host'] = self.host
            headers['Origin'] = self.origin
            headers['X-Requested-With'] = 'XMLHttpRequest'
            headers['Content-Type'] = 'application/x-www-form-urlencoded'
            headers['Connection'] = 'keep-alive'

            data = {}
            data['siteId'] = self.siteID['home']
            data['clientDevice'] = clientDevice
            data['st'] = self.dateToTime(startDate)
            data['et'] = self.dateToTime(endDate)
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

        def isLogin(self):
            try:
                time.sleep(1)
                wait = WebDriverWait(self.driver, 10)
                element = wait.until(EC.presence_of_element_located(
                    (By.ID, 'ErrorTip')))
                print 'Login Failed';
                return False
            except NoSuchElementException:
                print 'Login Successful';
                return True
            except TimeoutException:
                print 'Login Successful';
                return True

        def dateToTime(self,date):
            result = int(time.mktime(datetime.datetime.strptime(date, "%Y-%m-%d").timetuple()) * 1000)
            return str(result)

if __name__=="__main__":
    crawler = BaiduCrawler()
    crawler.start()
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq
import urllib
import urllib2
import cookielib

driver = webdriver.Chrome()
driver.get('http://tongji.baidu.com/web/welcome/login')

element = driver.find_element_by_class_name("login-trigger")
element.click();

element = driver.find_element_by_id("UserName")
element.send_keys("insta360")

element = driver.find_element_by_id("Password")
element.send_keys("******")

element = driver.find_element_by_id("Valicode")
input = raw_input("Please input valicode:");
element.send_keys(input)

element = driver.find_element_by_id("Submit")
element.click();

wait = WebDriverWait(driver, 30)
element = wait.until(EC.presence_of_element_located((By.XPATH,'//a[@href="/web/10551064/trend/time?siteId=6856127&flag=yesterday"]')))
element.click();

# PC
wait = WebDriverWait(driver, 30)
element = wait.until(EC.presence_of_element_located((By.ID,'tangram-checkGroup--TANGRAM__j-pc')))
element.click();

wait = WebDriverWait(driver, 30)
wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='simple_date_title']/div")))

html = driver.page_source
doc = pq(html)
items = doc('.line')
for item in items.items():
    trs = item.find('.td-content');
    for tr in trs.items():
        print tr.text();

# items = doc('tfoot').find("td")
# for item in items.items():
#     print item.text();











# cookies = driver.get_cookies()
# print(cookies)

# cookie = cookielib.MozillaCookieJar("C:\Users\Administrator\AppData\Local\Google\Chrome\User Data\Default\Cookies")
# opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
# url = 'http://tongji.baidu.com/web/10551064/trend/time?siteId=6856127&flag=yesterday'
# user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
# request = urllib2.Request(url)
# result = opener.open(request)
# print(result.read())

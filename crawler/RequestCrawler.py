from selenium import webdriver
import urllib
import urllib2
import json

driver = webdriver.Chrome()
driver.get('http://tongji.baidu.com/web/welcome/login')

element = driver.find_element_by_class_name("login-trigger")
element.click();

element = driver.find_element_by_id("UserName")
element.send_keys("insta360")

element = driver.find_element_by_id("Password")
element.send_keys("Kokiakiko123")

element = driver.find_element_by_id("Valicode")
input = raw_input("Please input valicode:");
element.send_keys(input)

element = driver.find_element_by_id("Submit")
element.click();

cookies = driver.get_cookies()
print cookies
temp = 'BAIDUID=7DDC1F27CA20A3B1D0A338F23CDE09A8:FG=1; BIDUPSID=7DDC1F27CA20A3B1D0A338F23CDE09A8; PSTM=1468217799; __cas__rn__=218399188; hm_usertype=0; hm_username=insta360; SIGNIN_UC=70a2711cf1d3d9b1a82d2f87d633bd8a02184029611; __cas__st__=828690ebbc20b3e67785e326d69d98357e73072683eab6c18b994f665a595ab2ee60d22c65af4330cf83d244; __cas__id__=10551064; '
for cookie in cookies:
    print "%s -> %s" % (cookie['name'], cookie['value'])
    temp = temp + cookie['name'] + ':' + cookie['value'] + ';'
print
cookie = temp


#day
url = 'http://tongji.baidu.com/web/10551064/ajax/post'
user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36'
# cookie = 'BAIDUID=7DDC1F27CA20A3B1D0A338F23CDE09A8:FG=1; BIDUPSID=7DDC1F27CA20A3B1D0A338F23CDE09A8; PSTM=1468217799; PRISON_COOKIE=5784510b6d73aa783c3a16a01786; pgv_pvi=9537885184; pgv_si=s5173361664; SFSSID=5f3ggtvtj7bochani6r5ps3jt6; H_PS_PSSID=1420_20537_20416_15246_12233; __cas__rn__=218399188; hm_usertype=0; hm_username=insta360; SIGNIN_UC=70a2711cf1d3d9b1a82d2f87d633bd8a02184029611; uc_login_unique=f272c48ecb533118dbcb97ea4c65b9bd; __cas__st__=828690ebbc20b3e67785e326d69d98357e73072683eab6c18b994f665a595ab2ee60d22c65af4330cf83d244; __cas__id__=10551064; Hm_lvt_09c5d4daddb9b6250ba93075257e58a2=1468289292,1468374824; Hm_lpvt_09c5d4daddb9b6250ba93075257e58a2=1468390515'

headers = {}
headers['User-Agent'] = user_agent
headers['Referer'] = 'http://tongji.baidu.com/web/10551064/trend/time?siteId=6856127&flag=month'
headers['Cookie'] = cookie
headers['Host'] = 'tongji.baidu.com'
headers['Origin'] = 'http://tongji.baidu.com'
headers['X-Requested-With'] = 'XMLHttpRequest'
headers['Content-Type'] = 'application/x-www-form-urlencoded'

startDate = '1465833600000'
endDate = '1468339200000'
data = {}
data['siteId'] = '6856127'
data['clientDevice'] = 'all'
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

try:
    request = urllib2.Request(url, urllib.urlencode(data),headers=headers)
    response = urllib2.urlopen(request)
    html = response.read()
    print html
    result = json.loads(html,encoding="utf-8")
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


###################################################
# 24hour
url = 'http://tongji.baidu.com/web/10551064/ajax/post'
user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36'
cookie = 'BAIDUID=7DDC1F27CA20A3B1D0A338F23CDE09A8:FG=1; BIDUPSID=7DDC1F27CA20A3B1D0A338F23CDE09A8; PSTM=1468217799; PRISON_COOKIE=5784510b6d73aa783c3a16a01786; pgv_pvi=9537885184; pgv_si=s5173361664; SFSSID=5f3ggtvtj7bochani6r5ps3jt6; H_PS_PSSID=1420_20537_20416_15246_12233; __cas__rn__=218399188; hm_usertype=0; hm_username=insta360; SIGNIN_UC=70a2711cf1d3d9b1a82d2f87d633bd8a02184029611; uc_login_unique=f272c48ecb533118dbcb97ea4c65b9bd; __cas__st__=828690ebbc20b3e67785e326d69d98357e73072683eab6c18b994f665a595ab2ee60d22c65af4330cf83d244; __cas__id__=10551064; Hm_lvt_09c5d4daddb9b6250ba93075257e58a2=1468289292,1468374824; Hm_lpvt_09c5d4daddb9b6250ba93075257e58a2=1468390515'
headers = {}
headers['User-Agent'] = user_agent
headers['Referer'] = 'http://tongji.baidu.com/web/10551064/trend/time?siteId=6856127&flag=yesterday'
headers['Cookie'] = cookie
headers['Host'] = 'tongji.baidu.com'
headers['Origin'] = 'http://tongji.baidu.com'
headers['X-Requested-With'] = 'XMLHttpRequest'
headers['Content-Type'] = 'application/x-www-form-urlencoded'

startDate = '1465833600000'
endDate = '1468339200000'
data = {}
data['siteId'] = '6856127'
data['clientDevice'] = 'all'
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

try:
    request = urllib2.Request(url, urllib.urlencode(data),headers=headers)
    response = urllib2.urlopen(request)
    html = response.read()
    result = json.loads(html,encoding="utf-8")
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
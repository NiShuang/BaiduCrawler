from pytesser import *
from PIL import Image
import ImageEnhance
import time
import datetime

# img = Image.open('screenshot.png')
# region = (471,473,551,513)
#
# cropImg = img.crop(region)
#
# cropImg.save('1.png')
#
# image = Image.open('1.png')  # Open image object using PIL
# print image_to_string(image)     # Run tesseract.exe on image
#
#
# image = Image.open('1.png')
# enhancer = ImageEnhance.Contrast(image)
# image_enhancer = enhancer.enhance(4)
# print image_to_string(image_enhancer)

# image = Image.open('1.png')
# enhancer = ImageEnhance.Contrast(image)
# image_enhancer = enhancer.enhance(2)
# print len(image_to_string(image_enhancer))
# print image_to_string(image_enhancer)

s = '2016-7-15'
result = int(time.mktime(datetime.datetime.strptime(s,"%Y-%m-%d").timetuple())*1000)
print str(result)
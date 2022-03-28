import datetime
from selenium.webdriver.chrome.service import Service

def normalize_month(a):
    if a<10:
        return "0"+str(a)
    else:
        return str(a)
def last_date(a):
    if a == 1 or a == 3 or a == 5 or a == 7 or a == 8 or a == 10 or a == 12:
        return "31"
    elif a == 2 and datetime.datetime.now().year % 4 == 0:
        return "29"
    elif a == 4 or a == 6 or a == 9 or a == 11:
        return "30"
    elif a == 2 and datetime.datetime.now().year % 4 != 0:
        return "28"

executed_path = ("C:\\Users\\bm.latypov\\Desktop\\python\\chromedriver.exe")
url_of_rosstat = "https://rosstat.gov.ru/price"
url_of_es = "https://appsso.eurostat.ec.europa.eu/nui/show.do?dataset=sts_inpp_m&lang=en"
url_of_metallplace_thisyear = "https://metallplace.ru/lme/lead/?firstdate=01." + normalize_month(datetime.datetime.now().month) + "." + str(datetime.datetime.now().year) + "&lastdate=" + last_date(datetime.datetime.now().month) + "." + normalize_month(datetime.datetime.now().month) + "." + str(datetime.datetime.now().year)
url_of_metallplace_lastyear = "https://metallplace.ru/lme/lead/?firstdate=01." + normalize_month(datetime.datetime.now().month) + "." + str(datetime.datetime.now().year-1) + "&lastdate=" + last_date(datetime.datetime.now().month) + "." + normalize_month(datetime.datetime.now().month) + "." +str(datetime.datetime.now().year-1)
url_of_asianmetal = "http://www.asianmetal.com/Graphite/"


def url():
    print(url_of_metallplace_thisyear)
    print(url_of_metallplace_lastyear)


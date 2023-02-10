from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import config
import datetime
import get_data_from_link



month = 1

executed_path = ("chromedriver.exe")


rosstat = "https://rosstat.gov.ru/statistics/price "
metallplace = "https://metallplace.ru/lme/lead/"
eurostat = 'https://ec.europa.eu/eurostat/databrowser/view/sts_inpp_m/default/table?lang=en'
asianmetal = "http://www.asianmetal.com/Graphite/"

start = datetime.datetime.now()
year = 2022
#get_data_from_link.get_rosstat_files(rosstat, executed_path)
#get_data_from_link.get_metallplace_data(metallplace, executed_path, month)
#get_data_from_link.get_eurostat_data(eurostat, executed_path, month)
get_data_from_link.get_asianmetal_data(asianmetal, executed_path, month, year)
print("Process end by " + str(datetime.datetime.now() - start))

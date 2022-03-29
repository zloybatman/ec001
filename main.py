from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import config
import datetime
import get_data_from_link
start = datetime.datetime.now()

get_data_from_link.get_rosstat_files()
#config.url()

get_data_from_link.get_metallplace_data()

get_data_from_link.get_eurostat_data()

get_data_from_link.get_asianmetal_data()

print("Process end by " + str(datetime.datetime.now() - start))

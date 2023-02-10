import glob
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import config
import datetime
import os
import pandas
import openpyxl


def normalize_month(a):
    if a < 10:
        return "0" + str(a)
    else:
        return str(a)


def last_date(a, year):
    if a == 1 or a == 3 or a == 5 or a == 7 or a == 8 or a == 10 or a == 12:
        return "31"
    elif a == 2 and int(year) % 4 == 0:
        return "29"
    elif a == 4 or a == 6 or a == 9 or a == 11:
        return "30"
    elif a == 2 and int(year) % 4 != 0:
        return "28"


def sel_click_xpath(driver, xpath, timeout=0):
    time.sleep(timeout)
    try:
        driver.find_element(By.XPATH, xpath).click()
        return True
    except Exception as ex:
        time.sleep(0.1)
        sel_click_xpath(driver, xpath, timeout)


def sel_click_text(driver, xpath, text, timeout=0, last=1):
    time.sleep(timeout)
    elements = driver.find_elements(By.XPATH, xpath)
    for element in elements:
        #print(element.text)
        if str(element.text) == text:
            element.click()
            if last != 0:
                break


def sel_text(driver, xpath, timeout=0):
    time.sleep(timeout)
    try:
        return driver.find_element(By.XPATH, xpath).text
    except Exception as ex:
        time.sleep(0.1)
        sel_text(driver, xpath, timeout)

def sel_write(driver, xpath, text, timeout=0):
    time.sleep(timeout)
    try:
        driver.find_element(By.XPATH, xpath).send_keys(text)
    except Exception as ex:
        time.sleep(0.1)
        sel_write(driver, xpath, text, timeout)
global wb

wb = openpyxl.load_workbook(filename="data from links.xlsx")
wb.worksheets[0]['A' + str(2 + int(wb.worksheets[0]['S1'].value))] = datetime.datetime.now().date()


def get_rosstat_files(url, webdriver_path):
    driver = webdriver.Chrome(executable_path=webdriver_path)
    try:
        driver.get(url=url)
        sel_click_xpath(driver,
                        "/html/body/main/section[2]/div/div/div/div/div/div/div[2]/div/div[7]/div/div[1]/div/div/div/div[1]/div/div[1]/a")
        sel_click_xpath(driver,
                        "/html/body/main/section[2]/div/div/div/div/div/div/div[2]/div/div[7]/div/div[1]/div/div/div/div[1]/div/div[2]/div/div/div/div[1]/div[1]/a",
                        0.1)
        sel_click_xpath(driver,
                        "/html/body/main/section[2]/div/div/div/div/div/div/div[2]/div/div[7]/div/div[1]/div/div/div/div[1]/div/div[2]/div/div/div/div[3]/div[1]/a")
        time.sleep(5)
    except Exception as ex:
        print(ex)
        driver.close()
        driver.quit()
        get_rosstat_files(url, webdriver_path)
    finally:
        driver.close()
        driver.quit()
    files()


def get_metallplace_data(url, webdriver_path, month=datetime.datetime.now().month):
    driver = webdriver.Chrome(executable_path=webdriver_path)
    try:
        url = url + "?firstdate=01." + normalize_month(month) + "." + str(
            datetime.datetime.now().year) + "&lastdate=" + last_date(month) + "." + normalize_month(month) + "." + str(
            datetime.datetime.now().year)
        driver.get(url=url)
        metallplace_this_year = sel_text(driver, "/html/body/div[5]/div/main/div[4]/div[2]/div[3]/div[2]/div")

        sel_click_xpath(driver, "/html/body/div[5]/div/main/form/div/div/div[1]/div[1]")
        for i in range(12):
            sel_click_xpath(driver,
                            "/html/body/div[5]/div/main/form/div/div/div[1]/div[2]/div/div/div/div[1]/nav/div[1]", 0.1)
        sel_click_text(driver,
                       "/html/body/div[5]/div/main/form/div/div/div[1]/div[2]/div/div/div/div[2]/div[1]/div[2]/div",
                       "1", 0.1)
        sel_click_xpath(driver, "/html/body/div[5]/div/main/form/div/div/div[2]/div[1]")
        for i in range(12):
            sel_click_xpath(driver,
                            "/html/body/div[5]/div/main/form/div/div/div[2]/div[2]/div/div/div/div[1]/nav/div[1]", 0.1)
        sel_click_text(driver,
                       "/html/body/div[5]/div/main/form/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div",
                       last_date(month), 0.1, 0)
        metallplace_last_year = sel_text(driver, "/html/body/div[5]/div/main/div[4]/div[2]/div[3]/div[2]/div", 3)

        metallplace_data = (((float(metallplace_this_year)/float(metallplace_last_year))) - 1)
        print(metallplace_data)

    except Exception as ex:
        print(ex)
        driver.close()
        driver.quit()
        get_metallplace_data(url, webdriver_path, month=datetime.datetime.now().month)
    finally:
        driver.close()
        driver.quit()


def get_asianmetal_data(asianmetal, executed_path, month, year):
    try:
        driver = webdriver.Chrome(executable_path=executed_path)

        driver.implicitly_wait(20)

        driver.get(url=asianmetal)

        driver.maximize_window()


        sel_click_xpath(driver, '//*[@id="loginbox"]/a/span')

        sel_write(driver, '//*[@id="cnopenloginname"]', "as.kharitonov@severstal.com")

        sel_write(driver, '//*[@id="cnopenloginpwd"]', "AM2019")

        sel_click_xpath(driver, '//*[@id="openloginbutn"]')

        sel_click_xpath(driver, '//*[@id="showBut"]/input[1]', 1) #//*[@id="showBut"]/input[2]

        sel_click_xpath(driver, '//*[@id="showBut"]/input', 1)

        sel_click_text(driver, '//*[@id="priceParamDiv"]/option', 'Graphite Electrode H.P. D400mm EXW China RMB/mt', 1)

        sel_click_text(driver, '//*[@id="strYear"]/option', str(int(year) - 1))

        sel_click_text(driver, '//*[@id="strMonth"]/option', month)

        sel_click_text(driver, '//*[@id="strDay"]/option', '1')

        sel_click_text(driver, '//*[@id="year"]/option', str(int(year) - 1))

        sel_click_text(driver, '//*[@id="month"]/option', month)

        sel_click_text(driver, '//*[@id="day"]/option', last_date(month, year))

        sel_click_xpath(driver, '//*[@id="subId1"]')

        time.sleep(100)

        driver.close()
        driver.quit()

    except Exception as ex:
        print(ex)
        driver.close()
        driver.quit()
        get_asianmetal_data()


def get_eurostat_data(url, webdriver_path, month):
    driver = webdriver.Chrome(executable_path=webdriver_path)
    try:
        driver.get(url=url)
        sel_click_xpath(driver, '//*[@id="time"]/div[1]/button/span', 15)
        key = 6
        while key < 100:

            try:
                sel_click_xpath(driver, '//*[@id="body"]/div[' + str(key) +  ']/div[1]/custom-extraction/div[2]/form/div/div/div/div/div[2]/div[1]/div/dimension-position-selector/div/div[3]/md-content[1]/div[2]/div/div[1]/button[2]')
                break
            except Exception as ex:
                i = i + 1
        sel_click_xpath(driver, '//*[@id="body"]/div[' + str(key) +  ']/div[1]/custom-extraction/div[2]/form/div/div/div/div/div[2]/div[1]/div/dimension-position-selector/div/div[3]/md-content[1]/div[2]/ng-include/div/div/button[2]')


        sel_click_xpath(driver, '//*[@id="rangeFromId"]')
        sel_write(driver, '//*[@id="search-term-for-time-from"]', str(datetime.datetime.now().year-2) + '-01')
        for i in range(1000):
            try:
                if driver.find_element(By.XPATH, '//*[@id="select_option_' + str(i) + '"]/div/span/span[1]/span/span').text == str(datetime.datetime.now().year-2) + '-01':
                    driver.find_element(By.XPATH, '//*[@id="select_option_' + str(i) + '"]/div/span/span[1]/span/span').click()
                    break
            except Exception as ex:
                print("", end = '')
        sel_click_xpath(driver, '//*[@id="rangeToId"]')
        for i in range(1000):
            try:
                driver.find_element(By.XPATH, '//*[@id="select_option_' + str(i) + '"]/div/span/span[1]/span').click()
                break
            except Exception as ex:
                print("", end = '')

        sel_click_xpath(driver, '//*[@id="body"]/div[' + str(key) +  ']/div[1]/custom-extraction/div[2]/form/div/div/div/div/div[2]/div[1]/div/dimension-position-selector/div/div[3]/md-content[1]/div[2]/ng-include/div/div/button[1]')
        sel_click_xpath(driver, '//*[@id="dimension-3"]/span')
        sel_click_xpath(driver, '//*[@id="embedded-Selector-nace_r2"]/div/div[2]/div[1]')
        sel_write(driver, '//*[@id="body"]/div[' + str(key) +  ']/div[1]/custom-extraction/div[2]/form/div/div/div/div/div[2]/div[1]/dimension-position-selector/div/div[3]/md-content[1]/div[2]/input', "c203")
        sel_click_xpath(driver, '//*[@id="embedded-Selector-nace_r2"]/div/div[2]/div/span/md-checkbox/div[1]')

        sel_click_xpath(driver, '//*[@id="dimension-1"]/span')
        sel_click_xpath(driver, '//*[@id="embedded-Selector-geo"]/div/div[2]/div[3]/span/md-checkbox/div[1]')
        sel_click_xpath(driver, '//*[@id="body"]/div[' + str(key) +  ']/div[1]/custom-extraction/div[2]/form/div/div/div/div/div[2]/div[1]/dimension-position-selector/div/div[3]/md-content[1]/div[4]/ng-include/div/div/button[3]')
        sel_click_xpath(driver, '//*[@id="dimension-6"]/span')
        sel_click_xpath(driver, '//*[@id="body"]/div[' + str(key) +  ']/div[1]/custom-extraction/div[2]/form/div/div/div/div/div[2]/div[1]/dimension-position-selector/div/div[3]/md-content[1]/div[3]/ng-include/div/div/button[3]')
        sel_click_xpath(driver, '//*[@id="body"]/div[' + str(key) +  ']/div[1]/custom-extraction/div[3]/table/tbody/tr/td[3]/button')
        time.sleep(10)
        sel_click_xpath(driver, '//*[@id="dropdownDownload"]')
        sel_click_xpath(driver, '//*[@id="xlsx__OnThisPageOnlyDownload"]')
        time.sleep(20)
        sel_click_xpath(driver, '//*[@id="time"]/div[1]/button/span')
        sel_click_xpath(driver, '//*[@id="dimension-3"]/span')
        sel_click_xpath(driver, '//*[@id="body"]/div[' + str(key+1) +  ']/div[1]/custom-extraction/div[2]/form/div/div/div/div/div[2]/div[1]/dimension-position-selector/div/div[3]/md-content[1]/div[4]/ng-include/div/div/button[2]')
        sel_write(driver, '//*[@id="body"]/div[' + str(key+1) +  ']/div[1]/custom-extraction/div[2]/form/div/div/div/div/div[2]/div[1]/dimension-position-selector/div/div[3]/md-content[1]/div[2]/input', "c232")

        sel_click_xpath(driver, '//*[@id="embedded-Selector-nace_r2"]/div/div[2]/div/span/md-checkbox/div[1]')
        sel_click_xpath(driver, '//*[@id="body"]/div[' + str(key+1) +  ']/div[1]/custom-extraction/div[3]/table/tbody/tr/td[3]/button/span')
        time.sleep(10)
        sel_click_xpath(driver, '//*[@id="dropdownDownload"]')
        sel_click_xpath(driver, '//*[@id="xlsx__OnThisPageOnlyDownload"]')
        time.sleep(30)


    except Exception as ex:
        print(ex)
        driver.close()
        driver.quit()
        get_eurostat_data(url, webdriver_path, month)
    finally:
        driver.close()
        driver.quit()


def files():
    paths = sorted(Path('C:\\Users\\bm.latypov\\Downloads').iterdir(),
                   key=os.path.getmtime)  # C:\\Users\\bm.latypov\\Downloads
    wb.worksheets[0]["B" + str(2 + int(wb.worksheets[0]['S1'].value))] = str(paths[len(paths) - 1])
    wb.worksheets[0]["C" + str(2 + int(wb.worksheets[0]['S1'].value))] = str(paths[len(paths) - 2])
    # (paths[len(paths) - 1])
    # print(paths[len(paths) - 2])

# f = open("text.txt", "w")
# import eurostat
# toc = eurostat.get_data('sts_inpp_m', True)
# f.write(str(toc))
# f.close()

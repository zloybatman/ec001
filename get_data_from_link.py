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

from selenium.common.exceptions import TimeoutException

global wb
wb = openpyxl.Workbook()
wb.create_sheet("Data from links", index=0)

def get_rosstat_files():
    driver = webdriver.Chrome(executable_path=config.executed_path)
    try:
       driver.get(url=config.url_of_rosstat)
       driver.find_element(By.LINK_TEXT, 'Цены производителей').click()
       time.sleep(0.1)
       driver.find_element(By.XPATH, "/html/body/main/section[2]/div/div/div/div/div/div/div[2]/div/div[3]/div/div[2]/div/div/div/div[1]/div/div[2]/div/div/div/div[1]/div/ul/li/div[2]/div/a").click()
       time.sleep(0.1)
       driver.find_element(By.XPATH, "/html/body/main/section[2]/div/div/div/div/div/div/div[2]/div/div[3]/div/div[2]/div/div/div/div[1]/div/div[2]/div/div/div/div[1]/div/ul/li/div[2]/ul/li/div/div/div/div[2]/div[2]/div[1]/a").click()
       time.sleep(0.1)
       driver.find_element(By.XPATH,"/html/body/main/section[2]/div/div/div/div/div/div/div[2]/div/div[3]/div/div[2]/div/div/div/div[1]/div/div[2]/div/div/div/div[1]/div/ul/li/div[2]/ul/li/div/div/div/div[5]/div[2]/div[1]/a").click()
       time.sleep(5)
    except Exception as ex:

         print(ex)
         driver.close()
         driver.quit()
         get_rosstat_files()
    finally:
        driver.close()
        driver.quit()
    files()
def get_metallplace_data():
    driver = webdriver.Chrome(executable_path=config.executed_path)
    try:
        driver.get(url=config.url_of_metallplace_thisyear)
        element = driver.find_element(By.XPATH, '//*[@id="price-index-information-tabs-1"]/div[2]/div/form/ul[2]/li[3]')
        wb.worksheets[0]["D2"] = (element.text.split(" ")[1])
        # print(element.text.split(" ")[1])
        driver.get(url=config.url_of_metallplace_lastyear)
        element = driver.find_element(By.XPATH, '//*[@id="price-index-information-tabs-1"]/div[2]/div/form/ul[2]/li[3]')
        wb.worksheets[0]["E2"] = (element.text.split(" ")[1])
        # print(element.text.split(" ")[1])
    except Exception as ex:
        print(ex)
        driver.close()
        driver.quit()
        get_metallplace_data()
    finally:
        driver.close()
        driver.quit()

def get_asianmetal_data():
    try:
        driver = webdriver.Chrome(executable_path=config.executed_path)
        driver.set_page_load_timeout(20)
        try:
            driver.get(url=config.url_of_asianmetal)

        except Exception as ex:
            print('', end='')
        finally:
            driver.maximize_window()
            driver.find_element(By.XPATH, '//*[@id="loginbox"]/a/span').click()

            driver.find_element(By.XPATH, '//*[@id="cnopenloginname"]').send_keys("as.kharitonov@severstal.com")

            driver.find_element(By.XPATH, '//*[@id="cnopenloginpwd"]').send_keys("AM2019")

            time.sleep(2)

            driver.find_element(By.XPATH, '//*[@id="openloginbutn"]').click()   #ok

            time.sleep(2)

            driver.find_element(By.XPATH, '//*[@id="showBut"]/input[1]').click()  #log on

            time.sleep(2)
            try:
                driver.find_element(By.XPATH, '//*[@id="showBut"]/input').click() #ok
                time.sleep(3)
            except Exception as ex:
                print("")
            finally:

                try:
                    element = driver.find_element(By.XPATH, '//*[@id="priceParamDiv"]/option[16]')
                except Exception as ex:
                    print("", end='')
                finally:
                    #print(element.text)
                    element.click()

                    driver.find_element(By.XPATH, ('//*[@id="strYear"]/option[' + str(23 + datetime.datetime.now().year-2022) + ']')).click()

                    driver.find_element(By.XPATH, ('//*[@id="strYear"]/option[' + str(23 + datetime.datetime.now().year - 2022) + ']')).click()

                    driver.find_element(By.XPATH, '//*[@id="strMonth"]/option[' + str(datetime.datetime.now().month - 1) +']').click()

                    driver.find_element(By.XPATH, '//*[@id="strDay"]/option[1]').click()

                    driver.find_element(By.XPATH, '//*[@id="year"]/option[' + str(23 + datetime.datetime.now().year-2022) + ']').click()

                    driver.find_element(By.XPATH, '//*[@id="month"]/option[' + str(datetime.datetime.now().month - 1) + ']').click()

                    driver.find_element(By.XPATH, '//*[@id="day"]/option[' + str(config.last_date(datetime.datetime.now().month - 1)) + ']').click()

                    driver.find_element(By.XPATH, '//*[@id="subId1"]').click()

                    time.sleep(5)
                    electrode_data = driver.find_element(By.XPATH, '//*[@id="mnthHghIdavg0"]')
                    wb.worksheets[0]["H2"] = electrode_data.text.replace(" ", "")
                    #print(electrode_data.text.replace(" ", ""))



                    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="priceParamDiv"]/option[8]')))
                    #print(element.text)
                    element.click()

                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="subId1"]'))).click()

                    time.sleep(5)

                    electrode_data = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="mnthHghIdavg0"]')))
                    wb.worksheets[0]["I2"] = electrode_data.text.replace(" ", "")
                    #print(electrode_data.text.replace(" ", ""))

                    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="priceParamDiv"]/option[10]')))
                    #print(element.text)
                    element.click()

                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="subId1"]'))).click()
                    time.sleep(5)

                    electrode_data = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="mnthHghIdavg0"]')))
                    wb.worksheets[0]["J2"] = electrode_data.text.replace(" ", "")
                    #print(electrode_data.text.replace(" ", ""))
                    driver.close()
                    driver.quit()
                    wb.save("data from links.xlsx")
    except Exception as ex:
        print(ex)
        driver.close()
        driver.quit()
        get_asianmetal_data()



def get_eurostat_data():
    driver = webdriver.Chrome(executable_path=config.executed_path)
    try:
        driver.get(url='https://appsso.eurostat.ec.europa.eu/nui/show.do?dataset=sts_inpp_m&lang=en')
        driver.find_element(By.XPATH, '//*[@id="TIME"]/button').click()
        driver.switch_to.window(driver.window_handles[1])
        time.sleep(1)
        driver.find_element(By.XPATH, '//*[@id="TIME' + str(datetime.datetime.now().year - 1) + '"]/a/ins').click()
        driver.find_element(By.XPATH, '//*[@id="TIME' + str(datetime.datetime.now().year - 1) + '"]/a/ins').click()
        driver.find_element(By.XPATH, '//*[@id="TIME' + str(datetime.datetime.now().year - 1) + '"]/a/ins').click()
        driver.find_element(By.XPATH, '//*[@id="tabs"]/div[1]/a/span').click()
        driver.find_element(By.XPATH, '//*[@id="checkUncheckAllCheckboxTable"]').click()
        driver.find_element(By.XPATH, '//*[@id="checkUncheckAllCheckboxTable"]').click()
        driver.find_element(By.XPATH, '//*[@id="ck_EA19"]').click()
        driver.find_element(By.XPATH, '//*[@id="tabs"]/div[3]/a/span').click()
        driver.find_element(By.XPATH, '//*[@id="ck_B-E36"]').click()
        driver.find_element(By.XPATH, '//*[@id="ck_C203"]').click()
        driver.find_element(By.XPATH, '//*[@id="tabs"]/div[6]/a/span').click()
        driver.find_element(By.XPATH, '//*[@id="checkUncheckAllCheckboxTable"]').click()
        driver.find_element(By.XPATH, '//*[@id="checkUncheckAllCheckboxTable"]').click()
        driver.find_element(By.XPATH, '//*[@id="ck_PCH_SM"]').click()
        driver.find_element(By.XPATH, '//*[@id="updateExtractionButton"]').click()
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(1)
        driver.maximize_window()
        wb.worksheets[0]["F2"] = driver.find_element(By.XPATH, '//*[@id="xtCut"]').text.split('\n')[len(driver.find_element(By.XPATH, '//*[@id="xtCut"]').text.split('\n'))-3]
        #print(driver.find_element(By.XPATH, '//*[@id="xtCut"]').text.split('\n')[len(driver.find_element(By.XPATH, '//*[@id="xtCut"]').text.split('\n'))-3])
        driver.find_element(By.XPATH, '//*[@id="TIME"]/button').click()
        driver.switch_to.window(driver.window_handles[1])
        time.sleep(1)
        driver.find_element(By.XPATH, '//*[@id="tabs"]/div[3]/a/span').click()
        driver.find_element(By.XPATH, '//*[@id="ck_C203"]').click()
        driver.find_element(By.XPATH, '//*[@id="ck_C232"]').click()
        driver.find_element(By.XPATH, '//*[@id="updateExtractionButton"]').click()
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(1)
        wb.worksheets[0]["G2"] = driver.find_element(By.XPATH, '//*[@id="xtCut"]').text.split('\n')[len(driver.find_element(By.XPATH, '//*[@id="xtCut"]').text.split('\n')) - 6]
        #print(driver.find_element(By.XPATH, '//*[@id="xtCut"]').text.split('\n')[len(driver.find_element(By.XPATH, '//*[@id="xtCut"]').text.split('\n')) - 6])
    except Exception as ex:
        print(ex)
        driver.close()
        driver.quit()
        get_eurostat_data()
    finally:
        driver.close()
        driver.quit()

def files():
    paths = sorted(Path('C:\\Users\\bm.latypov\\Downloads').iterdir(), key=os.path.getmtime)        #C:\\Users\\bm.latypov\\Downloads
    wb.worksheets[0]["B2"] = str(paths[len(paths) - 1])
    wb.worksheets[0]["C2"] = str(paths[len(paths) - 2])
    #(paths[len(paths) - 1])
    #print(paths[len(paths) - 2])


#f = open("text.txt", "w")
#import eurostat
#toc = eurostat.get_data('sts_inpp_m', True)
#f.write(str(toc))
#f.close()

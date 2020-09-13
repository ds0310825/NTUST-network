# import numpy as np
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from hidden_driver import HiddenChromeWebDriver

'''
launch the driver
search and get data
then? quit
again and again...
'''


def search():
    # options = Options()
    # options.add_argument('--headless')
    # driver = webdriver.Chrome(chrome_options=options)
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = HiddenChromeWebDriver(chrome_options=options)
    driver.get(r"https://network.ntust.edu.tw/")
    driver.implicitly_wait(10)
    total_internet_usage_item = driver.find_element_by_xpath(r'//*[@id="flowgrid"]/div[2]/table/tbody/tr[1]/td[6]')
    total_internet_usage = total_internet_usage_item.text[:-4]
    total_internet_usage = total_internet_usage.replace(',', '')

    total_internet_usage = int(total_internet_usage)
    total_internet_usage = total_internet_usage / 1024**2
    print(total_internet_usage.__str__()[:5], ' GByte')
    driver.quit()

    total_internet_usage = '{:.7f}'.format(total_internet_usage)[:5]

    print(total_internet_usage)
    return total_internet_usage

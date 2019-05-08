from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
import time
import re
import csv

#define function to read csv
def open_csv(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    return lines

#define function to convert dollar amount to float
def convert_num(strs):
	float_ = float(strs.replace('$','').replace(',',''))
	return float_

#read scaped links from scrapy file
urls = open_csv('bh_links.csv')[1:]

#set driver and initiate csv file to store result
driver = webdriver.Chrome(r'D:\chromedriver_win32\chromedriver.exe')
csv_file = open('specs.csv', 'a', encoding='utf-8', newline='')
writer = csv.writer(csv_file)

for url in urls:
	driver.get(url)

	WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="ui-id-2"]'))).click()
	review_dict = {}
	#----------------------------------------------------------------------------------------------------------
	brand = driver.find_element_by_xpath('//*[@id="tMain"]/div[1]/div[2]/h1/span[1]').text.strip()
	name = driver.find_element_by_xpath('//*[@id="tMain"]/div[1]/div[2]/h1/span[2]').text.strip()
	mfr_num = driver.find_element_by_xpath('//*[@id="tMain"]/div[1]/div[2]/span/span[2]').text.strip().split('#')[1].strip()

	review_dict['brand'] = brand
	review_dict['name'] = name
	review_dict['mfr_num'] = mfr_num

	time.sleep(3)
	try:
		specTopic = list(map(lambda x: x.text.strip(), driver.find_elements_by_xpath('//table[@class="specTable"]/tbody/tr/td[@data-selenium="specTopic"]')))
		specDetail = list(map(lambda x: x.text.strip(), driver.find_elements_by_xpath('//table[@class="specTable"]/tbody/tr/td[@data-selenium="specDetail"]')))
		conbine = list(zip(specTopic, specDetail))
		for i, j in conbine:
			review_dict[i] = j
		print(review_dict)
	except:
		continue


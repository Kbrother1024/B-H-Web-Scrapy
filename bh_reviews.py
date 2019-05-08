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
urls = open_csv('bh_links.csv')[10:]

#set driver and initiate csv file to store result
driver = webdriver.Chrome(r'D:\chromedriver_win32\chromedriver.exe')
csv_file = open('reviews.csv', 'a', encoding='utf-8', newline='')
writer = csv.writer(csv_file)

for url in urls:
	driver.get(url)
	time.sleep(1)
	try:
		show_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//span[@class="js-toggleShow js-viewAllHighlights c31 cursor-pointer view-all-highlights underline-on-hover js-show"]/span[1]')))
		show_button.click()
	except:
		continue
	brand = driver.find_element_by_xpath('//*[@id="tMain"]/div[1]/div[2]/h1/span[1]').text.strip()
	name = driver.find_element_by_xpath('//*[@id="tMain"]/div[1]/div[2]/h1/span[2]').text.strip()
	mfr_num = driver.find_element_by_xpath('//*[@id="tMain"]/div[1]/div[2]/span/span[2]').text.strip().split('#')[1].strip()
	try:
		final_price = convert_num(driver.find_elements_by_xpath('//span[@class="itc-you-pay-price bold"]')[1].text.strip())
	except:
		final_price = None
	
	try:
		product_info = ' --- '.join(list(map(lambda x: x.text.strip(),driver.find_elements_by_xpath('//ul[@class="top-section-list"]/li'))))
	except:
		product_info = 'Coming Soon'
	try:
		reg_price = convert_num(driver.find_element_by_xpath('//div[@class="pPrice"]/p[1]').text.strip().split('$')[1])
		saving = convert_num(driver.find_element_by_xpath('//span[@class="c32 OpenSans-600-normal"]').text.strip())
	except:
		reg_price = final_price
		saving = 0

	time.sleep(3)
	driver.find_element_by_xpath('//*[@id="ui-id-4"]').click()
	time.sleep(1)
	index = 1
	while True:
		try:
			print('try ', str(index))
			index+=1
			wait_button = WebDriverWait(driver, 10)
			next_button = wait_button.until(EC.element_to_be_clickable((By.XPATH,'//div[@class="reviews_load_more_button"]')))
			next_button.click()
			time.sleep(3)
		except:
			break
	reviews = driver.find_elements_by_xpath('//div[@class="reviews_review_wrapper reviews_parent_key"]')
	times = 1
	if reviews != []:
		for review in reviews:
			print('time ' + str(times))
			times+=1
			review_dict = {}
			review_dict['brand'] = brand
			review_dict['name'] = name
			review_dict['mfr_num'] = mfr_num
			review_dict['final_price'] = final_price
			review_dict['reg_price'] = reg_price
			review_dict['saving'] = saving
			review_dict['product_info'] = product_info

			try:
				re_verified = review.find_element_by_xpath('.//div[@class="reviews_review_verified"]').text.strip()
				re_title = review.find_element_by_xpath('.//div[@class="reviews_review_title allow_copy"]').text.strip()
				re_date_reviewed = review.find_element_by_xpath('.//div[@class="reviews_review_date"]').text.strip()
				try:
					re_username = review.find_element_by_xpath('.//div[@class="reviews_review_by"]/span').text.strip()
				except:
					re_username = 'dummy'
				re_text = review.find_element_by_xpath('.//div[@class="reviews_review_description allow_copy"]').text.strip()
				re_helpful = review.find_element_by_xpath('.//div[@class="reviews_review_up vote-button"]/span').text.strip()
				re_unhelpful = review.find_element_by_xpath('.//div[@class="reviews_review_down vote-button"]/span').text.strip()
				re_rating = list(map(lambda x: x.get_attribute('class'), review.find_elements_by_xpath('.//div[@class="reviews_review_stars_container"]/div')))
				re_rating = re_rating.count('review_rating_star_green')
			except:
				continue

			review_dict['re_verified'] = re_verified
			review_dict['re_title'] = re_title
			review_dict['re_date_reviewed'] = re_date_reviewed
			review_dict['re_username'] = re_username
			review_dict['re_text'] = re_text
			review_dict['re_helpful'] = re_helpful
			review_dict['re_unhelpful'] = re_unhelpful
			review_dict['re_rating'] = re_rating

			#writer.writerow(review_dict.values())
			print(review_dict)
	else:
		review_dict = {}
		review_dict['brand'] = brand
		review_dict['name'] = name
		review_dict['mfr_num'] = mfr_num
		review_dict['final_price'] = final_price
		review_dict['reg_price'] = reg_price
		review_dict['saving'] = saving
		review_dict['product_info'] = product_info
		review_dict['re_verified'] = None
		review_dict['re_title'] = None
		review_dict['re_date_reviewed'] = None
		review_dict['re_username'] = None
		review_dict['re_text'] = None
		review_dict['re_helpful'] = None
		review_dict['re_unhelpful'] = None
		review_dict['re_rating'] = None
		#writer.writerow(review_dict.values())
		print(review_dict)
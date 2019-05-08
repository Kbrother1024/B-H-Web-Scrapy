from scrapy import Spider, Request
from bh.items import BhItem
import re

class BhSpider(Spider):
	name = 'bh_spider'
	allowed_urls = ['https://www.bhphotovideo.com/']
	start_urls = ['https://www.bhphotovideo.com/c/buy/laptops/ci/18818/N/4110474292']

	def parse(self, response):

		page_info = response.xpath('//div[@class="twelve c2"]/p/text()').extract_first()
		num_pages = int(re.findall('\d+', page_info)[1])
		url_each_pages = ['https://www.bhphotovideo.com/c/buy/laptops/ci/18818/N/4110474292/pn/{}'.format(x) for x in range(1, num_pages+1)]

		for url in url_each_pages:
			yield Request(url = url, callback= self.parse_each_pages)

	def parse_each_pages(self, response):
		url_each_links = response.xpath('//div[@class="headder sect clearfix"]/h5/a[1]/@href').extract()
		for url in url_each_links:
			item = BhItem()
			item['url'] = url
			yield item

from returnData.items import indexItem
from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
import unicodedata

class DJIspider(CrawlSpider):
	name='dji'
	allowed_domains=['au.finance.yahoo.com']
	start_urls=['https://au.finance.yahoo.com/q/hp?s=^DJI']
	#/q/hp?s=^DJI&a=0&b=29&c=1985&d=8&e=22&f=2014&g=d&z=66&y=0
	
	rules=(
		Rule(LinkExtractor(allow=(), restrict_xpaths=('//a[@rel="next"]',)), callback='parse_data', follow=True),
		)

	def parse_start_url(self, response):
		return self.parse_data(response)
	
	def parse_data(self, response):
		hxs = Selector(response)
		rows = hxs.xpath('//table[@class="yfnc_datamodoutline1"]//table[@cellspacing="1"]/tr')
		item = indexItem()
		for r in rows[1:-1]:
			column = r.xpath('./td[@class="yfnc_tabledata1"]/text()').extract()
			item['date'] = column[0]
			item['adjclose'] = column[6]
			#print type(column[6])
			#item['link'] = response.url
			yield item
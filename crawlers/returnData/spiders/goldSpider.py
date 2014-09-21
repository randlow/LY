import scrapy
import json
from returnData.items import ReturndataItem

class GoldSpider(scrapy.Spider):
	name = "gold"
	allowed_domains = ["www.bloomberg.com"]
	start_urls = ["http://www.bloomberg.com/markets/chart/data/1Y/XAUUSD:CUR"]

	def parse(self, response):
		data=json.loads(response.body_as_unicode())

		item=ReturndataItem()

		daily = data["data_values"]
		
		for d in daily:
			item['closeprice']=d[1]
			item['epochtime']=d[0]
			yield item

import re
import scrapy
from scrapy.loader import ItemLoader
from ..items import SierraItem
from itemloaders.processors import TakeFirst

pattern = r'(\xa0)?'

class SierraSpider(scrapy.Spider):
	name = 'sierra'
	start_urls = ['https://www.bankofthesierra.com/about/news/']

	def parse(self, response):
		post_links = response.xpath('//h3/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		date = response.xpath('//h4/text()').get()
		title = response.xpath('//h1/text()').get()
		content = response.xpath('//div[@class="mod-news-detail"]//text()[not (ancestor::h4 or ancestor::a[@class="btn-orange-barrow"])]').getall()
		content = [p.strip() for p in content if p.strip()]
		content = re.sub(pattern, "",' '.join(content))

		item = ItemLoader(item=SierraItem(), response=response)
		item.default_output_processor = TakeFirst()

		item.add_value('title', title)
		item.add_value('link', response.url)
		item.add_value('content', content)
		item.add_value('date', date)

		yield item.load_item()

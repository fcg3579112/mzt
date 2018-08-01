import scrapy
import os.path

class MZSpider(scrapy.Spider):

    name = "mzt"

    def start_requests(self):
        urls = [
            'http://mzitu.com/xinggan/1',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse ,dont_filter=True)

    def parse(self, response):
    	list = response.xpath('//div[@class="postlist"]//a[@href]').re('http://www.mzitu.com/\d{5,6}')
    	for url in list:
    		yield scrapy.Request(url=url, callback=self.parseItemInfo ,dont_filter=True)
    		break

    def parseItemInfo(self, response):
    	max_page = response.xpath('//div[@class="pagenavi"]//span/text()')[-2].extract()
    	img = response.xpath('//div[@class="main-image"]//a/img')
    	url = img.xpath('@src').extract_first()
    	title = img.xpath('@alt').extract_first()
    	components = url.split('/')
    	print(title)
    	print(os.getcwd())
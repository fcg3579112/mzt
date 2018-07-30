import scrapy

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
    	print(list)
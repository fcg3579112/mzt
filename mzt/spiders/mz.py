import scrapy
import os.path

class MZSpider(scrapy.Spider):

    name = "mzt"

    def start_requests(self):
        urls = [
            'http://mzitu.com/xinggan/2',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse ,dont_filter=True)

    def parse(self, response):
    	list = response.xpath('//div[@class="postlist"]//a[@href]').re('http://www.mzitu.com/\d{6}')
    	for url in list:
    		yield scrapy.Request(url=url, callback=self.parseItemInfo ,dont_filter=True)
    		break

    def parseItemInfo(self, response):
    	max_page = response.xpath('//div[@class="pagenavi"]//span/text()')[-2].extract()
    	img = response.xpath('//div[@class="main-image"]//a/img')
    	title = img.xpath('@alt').extract_first()
    	self.makeDir(title)
    	for page in range(1,int(max_page) + 1):
    		url = response.url
    		if page != 1:
	    		url = response.url + '/' + str(page)
    		yield scrapy.Request(url=url, callback=self.parsePicUrl, dont_filter=True)
    		break

    def makeDir(self, file_name):
    	dir = os.path.join(os.getcwd(),"pics",file_name)
    	if not os.path.exists(dir):
    		os.makedirs(dir)
    	
    def parsePicUrl(self, response):
    	referer = response.url
    	img = response.xpath('//div[@class="main-image"]//a/img')
    	title = img.xpath('@alt').extract_first()
    	url = img.xpath('@src').extract_first()
    	meta = {'title':title}
    	yield scrapy.Request(url=url, callback=self.parsePicInfo,meta=meta, dont_filter=True)

    def parsePicInfo(self, response):
    	self.writeFile(response.body,response.url,response.meta['title'])
    	

    def writeFile(self,pic_data,url,title):
    	print(title)
    	filename = url.split('/')
    	filename = filename[-3] + filename[-2] + filename[-1]
    	file_path = os.path.join(os.getcwd(),'pics',title,filename)
    	with open(file_path, 'wb') as f:
    		f.write(pic_data)

    	
import scrapy
import os.path
file_dir = "pics"
class MZSpider(scrapy.Spider):
    

    name = "mzt"
    

    def start_requests(self):
        urls = list()
        for page in range(1,100):
            urls.append('http://mzitu.com/xinggan/page/' + str(page))

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse ,dont_filter=True)

    def parse(self, response):
        urls = response.xpath('//div[@class="postlist"]//li/a/@href').extract()
        titles = response.xpath('//div[@class="postlist"]//li//img/@alt').extract()
        for (url,title) in zip(urls,titles):
            yield scrapy.Request(url=url, callback=self.parseItemInfo ,meta={'title':title},dont_filter=True)
        
    def parseItemInfo(self, response):
    	max_page = response.xpath('//div[@class="pagenavi"]//span/text()')[-2].extract()
    	title = response.meta['title'].replace(' ','_')
    	self.makeDir(title)
    	for page in range(1,int(max_page) + 1):
    		url = response.url
    		if page != 1:
	    		url = response.url + '/' + str(page)
    		yield scrapy.Request(url=url, callback=self.parsePicUrl, meta={'title':title},dont_filter=True)
    		
    def makeDir(self, file_name):
    	dir = os.path.join(os.getcwd(),file_dir,file_name)
    	if not os.path.exists(dir):
    		os.makedirs(dir)
    	
    def parsePicUrl(self, response):
    	referer = response.url
    	url = response.xpath('//div[@class="main-image"]//a/img/@src').extract_first()
    	meta = {'title':response.meta['title']}
    	yield scrapy.Request(url=url, callback=self.parsePicInfo,meta=meta, dont_filter=True)

    def parsePicInfo(self, response):
    	self.writeFile(response.body,response.url,response.meta['title'])
    	
    def writeFile(self,pic_data,url,title):
        print(title)
        filename = url.split('/')
        filename = filename[-3] + '_' + filename[-2] + '_' + filename[-1]
        text_file_path = os.path.join(os.getcwd(),file_dir,title,title + '.text')
        file_path = os.path.join(os.getcwd(),file_dir,title,filename)

        with open(text_file_path,'a') as fm:
            fm.write('\n' + url)
            fm.close()
        with open(file_path, 'wb') as f:
            f.write(pic_data)
            f.close()

    	
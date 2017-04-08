import scrapy 

class DebateSpider(scrapy.Spider):
    name = 'debate-spider'
    start_urls = ['http://www.presidency.ucsb.edu/debates.php']

    def parse(self, response):
        text = ''
        paragraph = None
        for paragraph in response.css('p::text').extract():
            text += paragraph + '\n'
        if paragraph is not None:
            yield {'title': response.xpath('//title/text()').extract_first(), 'content': text}

        for link in response.css('td.doctext > a').xpath('@href').extract():
            yield scrapy.Request(response.urljoin(link), callback=self.parse)

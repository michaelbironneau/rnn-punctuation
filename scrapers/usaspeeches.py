import scrapy 

class SpeechSpider(scrapy.Spider):
    name = 'speech-spider'
    start_urls = ['http://www.speeches-usa.com/index.html']

    def parse(self, response):
        text = ''
        paragraph = None
        for paragraph in response.css('p.resourceBody::text').extract():
            text += paragraph + '\n'
        if paragraph is not None:
            yield {'title': response.xpath('//title/text()').extract_first(), 'content': text}

        for link in response.css('td.ListText > a').xpath('@href').extract():

            yield scrapy.Request(response.urljoin(link), callback=self.parse)

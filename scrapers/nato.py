import scrapy 

class DebateSpider(scrapy.Spider):
    name = 'debate-spider'
    start_urls = ['http://www.nato.int/cps/en/natohq/opinions.htm']

    def parse(self, response):
        text = ''
        paragraph = None
        for paragraph in response.css('div > p::text').extract():
            text += paragraph + '\n'
        if paragraph is not None:
            yield {'title': response.xpath('//title/text()').extract_first(), 'content': text}

        for link in response.css('h3 > a.bold').xpath('@href').extract():
            yield scrapy.Request(response.urljoin(link), callback=self.parse)

        next_link = response.css('a.pager-next').xpath('@href').extract_first()

        if next_link:
            yield scrapy.Request(response.urljoin(next_link), callback=self.parse)

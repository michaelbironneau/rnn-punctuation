import scrapy 

class DebateSpider(scrapy.Spider):
    name = 'debate-spider'
    start_urls = ['https://www.whitehouse.gov/briefing-room/speeches-and-remarks']

    def parse(self, response):
        text = ''
        paragraph = None
        for paragraph in response.css('div.field-item > p').extract():
            text += paragraph + '\n'
        if paragraph is not None:
            yield {'title': response.xpath('//title/text()').extract_first(), 'content': text}

        for link in response.css('h3.field-content > a').xpath('@href').extract():
            yield scrapy.Request(response.urljoin(link), callback=self.parse)

        next_link = response.css('li.pager-next > a').xpath('@href').extract_first()

        if next_link:
            yield scrapy.Request(response.urljoin(next_link), callback=self.parse)

import scrapy
from scrapy.http import Request

class GlassDoorSpider(scrapy.Spider):
    name = 'glassdoor'
    start_url = ['https://www.glassdoor.com.br/Avalia%C3%A7%C3%B5es/s%C3%A3o-paulo-avalia%C3%A7%C3%B5es-SRCH_IL.0,9_IM1009.htm']

# Apenas empresas de São Paulo

    def parse(self, response):
        link_lista = response.xpath('.//div[@class="eiHdrModule module snug "]')
        for link in link_lista:
            empresa = link.xpath('.//a[@class="tightAll h2"]/text()').get()
            nota = link.xpath('.//span[@class = "bigRating strong margRtSm h2"]/text()').get()
            avaliacoes = link.xpath('.//a[@class="eiCell cell reviews"]/span[@class="num h2"]/text()').get()
            yield {
                'empresa': empresa,
                'nota': nota,
                'avaliacoes': avaliacoes,
            }
        pages_url = response.css('.next a::attr(href)').get()
        yield Request('https://www.glassdoor.com.br' + pages_url, callback=self.parse)


#scrapy runspider GlassdoorLucas.py -s HTTPCACHE_ENABLE=1 -o glass.csv

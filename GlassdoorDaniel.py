# Scrapy como ferramenta de Spider/Crawler para mineração dos dados
import scrapy
from scrapy.http import Request

# Passando como parâmetro inicial seu link de início, que tem São Paulo como cidade em sua busca.
class GlassDoorSpider(scrapy.Spider):
    name = 'glassdoor'
    start_url = ['https://www.glassdoor.com.br/Avalia%C3%A7%C3%B5es/s%C3%A3o-paulo-avalia%C3%A7%C3%B5es-SRCH_IL.0,9_IM1009.htm']


    def parse(self, response):  # Função Parse que recebe o response como parâmetro
        link_lista = response.xpath('.//div[@class="eiHdrModule module snug "]')
        for link in link_lista:   # Loop para pegar a empresa/ nota e avaliação pois em cada página temos 10 empresas
            empresa = link.xpath('.//a[@class="tightAll h2"]/text()').get()
            nota = link.xpath('.//span[@class = "bigRating strong margRtSm h2"]/text()').get()
            avaliacoes = link.xpath('.//a[@class="eiCell cell reviews"]/span[@class="num h2"]/text()').get()
            yield {
                'empresa': empresa,
                'nota': nota,
                'avaliacoes': avaliacoes,
            }
        pages_url = response.css('.next a::attr(href)').get() # Pega a o url da próxima página na variável pages_url
        yield Request('https://www.glassdoor.com.br' + pages_url, callback=self.parse) # Junta o ulr do site com a próxima página e chama a função parse   


# scrapy runspider GlassdoorDaniel.py -s HTTPCACHE_ENABLE=1 -o glass.csv

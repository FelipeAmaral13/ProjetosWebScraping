import scrapy
from ..items import TripadvisorItem

class ComentariosSpider(scrapy.Spider):
    name = 'comentarios'
    allowed_domains = ['https://www.tripadvisor.com.br/']
    start_urls = ['https://www.tripadvisor.com.br/Attraction_Review-g303441-d553398-Reviews-Parque_Barigui-Curitiba_State_of_Parana.html']

    def parse(self, response):
        item = TripadvisorItem()
        quadros_de_comentarios = response.xpath("//div[@class='Dq9MAugU T870kzTX LnVzGwUB']")

        for quadro in quadros_de_comentarios:
            item['autor_comentario'] = quadro.xpath(".//span/a[@class='ui_header_link _1r_My98y']/text()").get()
         
         
        for comentario in quadros_de_comentarios:
            item['comentario'] = comentario.xpath(".//div[@class='_2f_ruteS _1bona3Pu _2uD5bLZZ']/text()").get()
        
        yield item


        

import scrapy

class Spudi(scrapy.Spider):
    name = "spudi"
    base_url = 'https://www.wildberries.ru/catalog/obuv/zhenskaya/sabo-i-myuli/myuli?page=%s'
    start_urls = [base_url % 1]

    def parse(self, response):
        next_page = 0
        for i in response.css('div.dtList'):
            size = False
            if (i.css('span.sizes').extract_first != None):
                size = True
            yield {
                # '': i.css('').extract_first(),
                'timestamp': None,
                'RPC': i.css('div::attr(id)').extract_first(),
                'url': i.css('a::attr(href)').extract_first(),
                'title': i.css('span.goods-name::text').extract_first(),
                'marketing_tags': None,
                'brand': i.css('strong.brand-name::text').extract_first(),
                'selection': response.css('div.breadcrumbs span::text').extract(),
                'price_data': 
                {
                    'current': i.css('del::text').extract_first(),
                    'origina': i.css('ins.lower-price::text').extract_first(),
                    'sale_tag': i.css('span.price-sale.active::text').extract_first(),
                },
                
                'stock':
                {
                    'in_stock': size,   
                },
                'assets':
                {
                    'main_image': i.css('div.l_class img::attr(data-original)').extract_first(),
                    'set_images': None,
                },
                'metadata': 
                {
                    '__description': None,
                },
            }
            next_page += 1
            yield scrapy.Request(self.base_url % next_page)
import json
import os
import re

import scrapy
from hkt_scrape.items import PhoneData


class ProductSpider(scrapy.Spider):
    name = 'products'

    def start_requests(self):
        urls = [
            # 'https://www.hkt.com/vgn-ext-templating/HKTCorpsite2/Template/Handsetsandtablets1.jsp?shop=1010&language=en_US',
            'https://www.hkt.com/vgn-ext-templating/HKTCorpsite2/Template/Handsetsandtablets1.jsp?shop=csl&language=en_US'
            # 'https://www.hkt.com/On%20the%20go/1010/Handsets+and+tablets?shop=1010&language=en_US'
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        product_details = response.css('a.link-label')
        handset_ids = self.get_tablethandset_item_ids(product_details)

        # self.get_tablethandset_details(handset_ids)

        # save the product ID numbers
        json_file = './data/product_ids.json'
        with open(json_file, 'w') as fp:
            json.dump(handset_ids, fp)
            print('saved file ', json_file)

    def get_tablethandset_item_ids(self, product_details):

        product_ids = []
        for detail in product_details:
            text = detail.css('a').extract_first()
            product_id = re.search('handsetId=[0-9]{3,10}', text)
            if product_id:
                product_id = product_id.group(0).split('=')[-1]
                product_ids.append(product_id)

        return product_ids

        # response.css('a.link-label')
        # product_detail.css('a').extract_first()


class ProductInfoSpider(scrapy.Spider):
    name = 'product_info'

    def start_requests(self):
        base_url = 'https://www.hkt.com/vgn-ext-templating/HKTCorpsite2/Template/IndividualDevice1.jsp?language=en_US&handsetId='
        # 'https://www.hkt.com/vgn-ext-templating/HKTCorpsite2/Template/IndividualDevice1.jsp?shop=1010&language=en_US&handsetId='
        json_file = './data/product_ids.json'

        with open(json_file) as json_data:
            product_ids = json.load(json_data)

        urls = [base_url + id_number for id_number in product_ids]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        product_number = response.url.split('=')[-1]
        product_name = response.css('h1.page-title::text').extract()[0].strip()
        img_url = response.css('img.img-responsive').xpath("@src").extract_first()

        product_dir = './data/products'
        if not os.path.exists(product_dir):
            os.mkdir(product_dir)

        product_detail = response.css('div.row.info-row')

        stripped_rows = [['product_name', product_name]]
        for row in product_detail:
            # find the divs
            row_info = row.css('div')
            stripped_entry = []
            stripped_entry_dict = {}
            for entry in row_info:
                text = entry.css('div::text').extract()

                for t in text:
                    stripped = t.strip()
                    if len(stripped) > 0 and stripped not in stripped_entry:
                        stripped_entry.append(stripped)

            stripped_rows.append(stripped_entry)

        feature_data = response.css('ul.features')
        for feat in feature_data:
            key_features = feat.css('li::text').extract_first().strip()
            stripped_rows.append(['key features', key_features])

        # yield {product_number : stripped_rows}
        price_reg = '([0-9\.]+)'
        price_data = response.css('p.font-arial-bold.srp::text').extract_first().strip()
        price = re.search(price_reg, price_data).group(0)
        stripped_rows.append(['price', price])

        yield PhoneData(image_urls=[img_url], metadata={product_number : stripped_rows})
        # import pdb
        # pdb.set_trace()

    #
    # def get_tablethandset_details(self, product_ids):
    #     print('in details')
    #
    #     for id in product_ids:
    #         this_url = base_url + id
    #         print(this_url)
    #         # yield scrapy.Request(url=this_url, callback=self.product_info)
    #
    #         print(' ')
    #
    #
    # def product_info(self, response):
    #     print(response)
    #     print('hello!')
    #     print(' ')
    #     import pdb
    #     pdb.set_trace()


    # https://www.hkt.com/vgn-ext-templating/HKTCorpsite2/Template/IndividualDevice1.jsp?shop=1010&language=en_US&handsetId=4903
    # response.css('div.row.info-row') #gets the product info

    '''on an individual product page .... 
    
    #product_detail = response.css('a.link-label')
    
    # product_detail = response.css('a.link-label')[15] 
    # text = product_detail.css('a').extract_first()
    # re.search('handsetId=[0-9]{3,10}', text).group(0)
    
    
    response.css('div.row.info-row')[1].css('div')[2].css('div::text')
    
    [1] is the row here (first thing selects the row)
    [2] the info ([1] in the second spot would be the label for the data))
    
    
    '''

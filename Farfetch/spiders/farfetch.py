import csv
import json
import re

import scrapy
from scrapy import Request


class FarfetchSpider(scrapy.Spider):
    name = 'farfetch'
    zyte_key = ''  # Todo : YOUR API KEY FROM ZYTE
    HTTPERROR_ALLOWED_CODES = [404, 503, 204]

    custom_settings = {
        'FEED_URI': 'farfetch.json',
        'FEED_FORMAT': 'json',
        'ZYTE_SMARTPROXY_ENABLED': True,
        'ZYTE_SMARTPROXY_APIKEY': zyte_key,
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy_zyte_smartproxy.ZyteSmartProxyMiddleware': 610
        },

    }
    base_url = 'https://www.farfetch.com'
    language_read = [lang['language'] for lang in csv.DictReader(open('language.csv', encoding='utf-8'))][0]
    language = '/es/' if 'spanish' in language_read else '/'
    url = f"https://www.farfetch.com{language}experience-gateway"
    payload = {
        "operationName": "getAvailabilityInfo",
        "variables": {
            "productId": "",
            "variationId": None
        },
        "query": "query getAvailabilityInfo($productId: ID!, $merchantId: ID, $sizeId: ID, $variationId: ID) "
                 "{\n  product(id: $productId, merchantId: $merchantId, sizeId: $sizeId) {\n    ... on Product {\n     "
                 "id\n      availableOffers {\n        id\n        image {\n          alt\n          url\n          "
                 "__typename\n        }\n        path\n        __typename\n      }\n      __typename\n    }\n    "
                 "__typename\n  }\n  variation(\n    productId: $productId\n    merchantId: $merchantId\n    sizeId: "
                 "$sizeId\n    variationId: $variationId\n  ) {\n    ... on Variation {\n      id\n      shipping {\n "
                 "       stockType\n        city {\n          id\n          name\n          __typename\n        }\n   "
                 "     fulfillmentDate\n        __typename\n      }\n      deliveryMethods(types: [STANDARD, EXPRESS, "
                 "SAME_DAY, NINETY_MINUTES]) {\n        type\n        order\n        purchaseDateInterval {\n          "
                 "start\n          end\n          __typename\n        }\n        estimatedDeliveryDateInterval {\n     "
                 "start\n          end\n          __typename\n        }\n        __typename\n      }\n      "
                 "availabilityTypes\n      __typename\n    }\n    __typename\n  }\n}\n"
    }
    headers = {
        'authority': 'www.farfetch.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9,de;q=0.8',
        'content-type': 'application/json',
        'cookie': 'ckm-ctx-sf=%2F;',
        'origin': 'https://www.farfetch.com',
        'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
        'x-ff-gql-c': 'true',
        'X-Crawlera-Region': 'us',
        'X-Crawlera-Profile': 'pass'
    }
    recommended_headers = {
        'authority': 'www.farfetch.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9,de;q=0.8',
        'cache-control': 'no-cache, no-store, must-revalidate',
        'referer': f'https://www.farfetch.com{language}shopping/women/ami-paris-sweatshirt-med-logotyp-item-17152180.aspx',
        'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36',
        'x-newrelic-id': 'VQUCV1ZUGwcHU1lXBAYBXg==',
        'x-requested-with': 'XMLHttpRequest',
        'X-Crawlera-Region': 'US',
        'cookie': 'ckm-ctx-sf=%2F;',
        'X-Crawlera-Profile': 'pass',
        'X-Crawlera-Cookies': 'disable',
    }
    rec_headers = {
        'authority': 'www.farfetch.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9,de;q=0.8',
        'cache-control': 'no-cache, no-store, must-revalidate',
        'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'cookie': 'ckm-ctx-sf=%2F;',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
        'X-Crawlera-Region': 'US',
        'X-Crawlera-Profile': 'pass'
    }
    look_url = f"https://www.farfetch.com{language}experience-gateway"
    look_payload = {
        "operationName": "ShopTheLook",
        "variables": {
            "productId": "18581509",
            "includeOutfitsDetails": True
        },
        "query": "query ShopTheLook($productId: ID!, $variationId: ID, $merchantId: ID, $sizeId: ID, "
                 "$includeOutfitsDetails: Boolean!) {\n  product(id: $productId, merchantId: $merchantId,"
                 " sizeId: $sizeId) {\n    ... on Product {\n      id\n      outfit {\n        totalCount\n "
                 "       edges @include(if: $includeOutfitsDetails) {\n          node {\n            ... on "
                 "AvailableOutfitItem {\n              ...AvailableOutfitItemFields\n              __typename\n"
                 "            }\n            ... on OutOfStockOutfitItem {\n              "
                 "...OutOfStockOutfitItemFields\n              __typename\n            }\n            __typename\n"
                 "          }\n          cursor\n          __typename\n        }\n        id\n        source\n"
                 "        outfitFlowDuration\n        __typename\n      }\n      brand {\n        id\n        "
                 "name\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  variation(\n"
                 "    productId: $productId\n    variationId: $variationId\n    merchantId: $merchantId\n    "
                 "sizeId: $sizeId\n  ) @include(if: $includeOutfitsDetails) {\n    ... on Variation {\n      id\n"
                 "      ...OutfitItemImages\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment "
                 "AvailableOutfitItemFields on AvailableOutfitItem {\n  item {\n    ... on Variation {\n      "
                 "...VariationFields\n      labels {\n        primary\n        secondary\n        __typename\n"
                 "      }\n      __typename\n    }\n    ... on VariationUnavailable {\n      "
                 "...VariationUnavailableFields\n      labels {\n        primary\n        secondary\n        "
                 "__typename\n      }\n      __typename\n    }\n    __typename\n  }\n  recommendationsStrategy\n  "
                 "outfitFlowDuration\n  __typename\n}\n\nfragment VariationFields on Variation {\n  id\n  "
                 "internalProductId\n  availabilityTypes\n  ...OutfitItemImages\n  ...OutfitItemPrice\n  "
                 "...OutfitItemDescription\n  variationProperties {\n    ... on ScaledSizeVariationProperty "
                 "{\n      order\n      values {\n        id\n        order\n        scale {\n          id\n"
                 "          description\n          __typename\n        }\n        __typename\n      }\n      "
                 "__typename\n    }\n    __typename\n  }\n  merchandiseLabelIds\n  resourceIdentifier {\n    "
                 "path\n    __typename\n  }\n  availabilityTypes\n  product {\n    id\n    brand {\n      id\n"
                 "      name\n      __typename\n    }\n    gender {\n      id\n      __typename\n    }\n    "
                 "variations {\n      totalCount\n      totalQuantity\n      edges {\n        node {\n          "
                 "... on Variation {\n            id\n            quantity\n            availabilityTypes\n"
                 "            ...Shipping\n            ...OutfitItemPrice\n            variationProperties {\n"
                 "              ... on ScaledSizeVariationProperty {\n                order\n                "
                 "values {\n                  id\n                  order\n                  description\n"
                 "                  scale {\n                    id\n                    abbreviation\n"
                 "                    description\n                    __typename\n                  }\n"
                 "                  __typename\n                }\n                __typename\n              "
                 "}\n              __typename\n            }\n            __typename\n          }\n          "
                 "__typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  "
                 "}\n  __typename\n}\n\nfragment OutfitItemImages on Variation {\n  images {\n    order\n    "
                 "size480 {\n      alt\n      url\n      __typename\n    }\n    __typename\n  }\n  "
                 "__typename\n}\n\nfragment OutfitItemPrice on Variation {\n  price {\n    value {\n      formatted\n"
                 "      raw\n      __typename\n    }\n    installments {\n      value {\n        formatted\n       "
                 " __typename\n      }\n      __typename\n    }\n    ... on SalePrice {\n      fullPriceValue {\n "
                 "       formatted\n        raw\n        __typename\n      }\n      discountPercentage {\n"
                 "        raw\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n"
                 "  __typename\n}\n\nfragment OutfitItemDescription on Variation {\n  description {\n    "
                 "short {\n      ... on TextDescription {\n        textContent\n        __typename\n      }\n"
                 "      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment Shipping on Variation "
                 "{\n  shipping {\n    merchant {\n      id\n      __typename\n    }\n    stockType\n    "
                 "__typename\n  }\n  __typename\n}\n\nfragment VariationUnavailableFields on VariationUnavailable "
                 "{\n  description {\n    short {\n      ... on TextDescription {\n        textContent\n        "
                 "__typename\n      }\n      __typename\n    }\n    __typename\n  }\n  images {\n    order\n    "
                 "size480 {\n      alt\n      url\n      __typename\n    }\n    __typename\n  }\n  resourceIdentifier "
                 "{\n    path\n    __typename\n  }\n  product {\n    id\n    brand {\n      id\n      name\n      "
                 "__typename\n    }\n    gender {\n      id\n      __typename\n    }\n    __typename\n  }\n  "
                 "__typename\n}\n\nfragment OutOfStockOutfitItemFields on OutOfStockOutfitItem {\n  item {\n    "
                 "... on Variation {\n      ...VariationFields\n      labels {\n        primary\n        "
                 "__typename\n      }\n      __typename\n    }\n    ... on VariationUnavailable {\n      "
                 "...VariationUnavailableFields\n      labels {\n        primary\n        __typename\n      "
                 "}\n      __typename\n    }\n    __typename\n  }\n  alternative {\n    ...AvailableOutfitItemFields\n"
                 "    __typename\n  }\n  recommendationsStrategy\n  __typename\n}\n"
    }
    look_headers = {
        'authority': 'www.farfetch.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9,de;q=0.8',
        'content-type': 'application/json',
        'origin': 'https://www.farfetch.com',
        'referer': f'https://www.farfetch.com/shopping/men/jil-sander-axelvaska-med-flatad-rem-item-18581509.aspx'
                   '?rtype=web_pdp_stl_io&rmodule=shop_the_look&rid=e9289019-cd84-4f71-9d59-4a2ddd29e196&rpos=2',
        'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'cookie': 'ckm-ctx-sf=%2F;',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.64 Safari/537.31',

        'x-ff-gql-c': 'true',
        'X-Crawlera-Region': 'US',
        'X-Crawlera-Profile': 'pass'
    }

    def start_requests(self):
        for row in list(csv.DictReader(open('input.csv', encoding='utf-8'))):
            yield Request(url=f"{self.base_url}{self.language}search?q={row['SKU'].replace('.', '')}{row['COLOR']}",
                          headers=self.headers,
                          callback=self.detail_page,
                          meta={
                              'color': row['COLOR'],
                              'p_id': row['SKU'],
                          })

    def detail_page(self, response):
        # if response.status == 200:
        images = re.findall('contentUrl":"(.+?)"', response.text)
        brand_name = response.css('[data-ffref="pp_infobrd"]::text').get('')
        sale_price = response.css('[data-component="PriceFinalLarge"]::text').get('')
        price = ''.join(response.css('[data-component="PriceOriginal"]::text').getall())
        description = ''.join(re.findall('"full\\\\":{\\\\"__typename\\\\":\\\\"TextDescription\\\\",\\\\"'
                                 'textContent\\\\":\\\\"(.+?)"', response.text))
        mini_description = response.css('p.ltr-13ze6d5-Body::text').getall()
        availability = response.css('[property="og:availability"]::attr(content)').get()
        currency = response.css('[property="og:price:currency"]::attr(content)').get()
        price_before_sale = response.css('[property="og:price:amount"]::attr(content)').get()
        price_value = price if price else sale_price
        # large_desc = ''.join(description).replace(brand_name, '').replace('mini_description', '').strip()
        highlights = response.css('._fdc1e5 li::text').getall()
        if '/es/' in response.url:
            made_in = response.xpath('//*[contains(text(),"Hecho en")]//text()').get('').replace('Hecho en ', '')
            composition = response.xpath('//h4[contains(text(),"Composición")]/ancestor::div[1]//p//text()').getall()
            washing = response.xpath('//h4[contains(text(),"Instrucciones de lavado")]/ancestor::div[1]//p//text()').getall()
            farfetch_id = response.xpath('//*[contains(text(),"ID de FARFETCH")]//*[contains(@dir,"ltr")]//text()').get('')
        else:
            made_in = response.xpath('//*[contains(text(),"Made in")]//text()').get('')
            composition = response.xpath('//h4[contains(text(),"Composition")]/ancestor::div[1]//p//text()').getall()
            washing = response.xpath('//h4[contains(text(),"Washing instructions")]/ancestor::div[1]//p//text()').getall()
            farfetch_id = response.xpath('//*[contains(text(),"FARFETCH ID")]//*[contains(@dir,"ltr")]//text()').get('')
        try:
            final_price = int(re.search(r'\d+', price_value.replace(',', '').replace('.', '')).group())
        except:
            final_price = 0

        data = {
            'sku': response.meta['p_id'],
            'Farfetch Id': farfetch_id.strip(),
            'Images': images,
            'brand': brand_name,
            'descriptionSmall': ''.join(mini_description) if mini_description else '',
            'actual price': price_before_sale,
            'sale Price': final_price,
            'currency': currency,
            'descriptionLarge': description.replace('\\',''),
            'highlights': highlights,
            'Composition': ' '.join(''.join(composition).split()).replace('Composition', ''),
            'Washing': ' '.join(''.join(washing).split()).replace('Washing instructions', ''),
            'madeIn': made_in.replace('Made in ', ''),
            'Availability': availability,
            'Color Code': response.meta['color'],
            'Url': response.url

        }
        # yield data
        url = f"https://www.farfetch.com{self.language}recommendations-slice/recommended-products?pageType=pdp&productId=" \
              f"{data['Farfetch Id']}&countryCode=/se&moduleType=recommendedProducts"
        yield Request(url=url,
                      callback=self.recommended_products,
                      headers=self.recommended_headers,
                      meta={'product': data},
                      dont_filter=True)

    def recommended_products(self, response):
        product = response.meta['product']
        try:
            json_data = json.loads(response.text).get('products', {})
            recommended_products = [product.get('productId', '') for product in json_data]
            product['Recommended Products'] = recommended_products
        except:
            product['Recommended Products'] = []
        self.look_payload['variables']['productId'] = product['Farfetch Id']
        yield Request(url=self.look_url,
                      method="POST",
                      headers=self.look_headers,
                      body=json.dumps(self.look_payload),
                      callback=self.complete_the_look,
                      dont_filter=True,
                      meta={'product': product,
                            })

    def complete_the_look(self, response):
        product = response.meta['product']
        try:
            json_loads = json.loads(response.text).get('data', {}).get('product', {})
            lookup_products = json_loads.get('outfit', {}).get('edges', {})
            lookup = [lookup.get('node', {}).get('item', {}).get('internalProductId', '') for lookup in lookup_products]
            product['Complete the look'] = lookup
        except:
            product['Complete the look'] = []
        if product['Farfetch Id']:
            yield product

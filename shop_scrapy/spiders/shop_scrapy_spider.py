import scrapy
from scrapy.shell import inspect_response
from ..items import PostItem
from urllib.parse import urlparse


class ShopScrapySpiderSpider(scrapy.Spider):
    name = 'shop_scrapy_spider'
    allowed_domains = ['shopping.yahoo.co.jp', 'rakuten.co.jp']
    # start_urls = ['https://store.shopping.yahoo.co.jp/y-lohaco/search.html?p=&X=4#CentSrchFilter1']

    def __init__(self, url='', maxpage=20, *args, **kwargs):
        super(ShopScrapySpiderSpider, self).__init__(*args, **kwargs)
        # 引数にURLを指定したものをstart_urlsとして設定する
        # 例)-a url='https://xxxx.com/yyyy'
        self.start_urls = [url]
        # 引数にURLを指定したものをMax pageとして設定する
        # 例)-a maxpage=5
        self.maxpage = maxpage
        self.page_counter = 0

    def parse(self, response):

        # ドメインが'rakuten.co.jp'か'shopping.yahoo.co.jp'かで場合分け
        url = response.url
        domain = urlparse(url).netloc
        print('ドメイン', domain)

        # Yahooの場合
        if 'yahoo.co.jp' in domain:
            # maxpageを超えないようにするためのページのカウンター設定
            self.page_counter += 1
            # 商品の要素を取得
            elems = response.xpath('//div[@class="elName"]')
            for elem in elems:
                yield response.follow(url=elem.xpath('.//a/@href').get(),
                                      callback=self.yahoo_parse_item)
            # 次のページのリンクを取得
            next_page = response.xpath('//li[@class="elNext"]/a/@href').get()

            # 次のページがあれば繰り返し
            if next_page and self.page_counter <= int(self.maxpage):
                yield response.follow(url=next_page, callback=self.parse)
        # 楽天の場合
        elif 'rakuten.co.jp' in domain:
            self.page_counter += 1
            elems = response.xpath('//div[@class="content title"]/h2')
            for elem in elems:
                yield response.follow(url=elem.xpath('.//a/@href').get(),
                                      callback=self.rakuten_parse_item)
            # 次のページのリンクを取得
            next_page = response.xpath('//div[@class="dui-pagination"]/a[@class="item -next nextPage"]/@href').get()

            # 次のページがあれば繰り返し
            if next_page and self.page_counter <= int(self.maxpage):
                yield response.follow(url=next_page, callback=self.parse)

    # Yahoo商品ページのパーサー
    def yahoo_parse_item(self, response):
        # priceのカンマを削除してint型に変換
        before_price = response.xpath('.//span[@class="elPriceNumber"]/text()').get()
        int_price = int(before_price.replace(',', ''))
        # Items.pyのPostItemへyieldする
        yield PostItem(
            title=response.xpath('.//p[@class="elName"]/text()').get(),
            price=int_price,
            jan=response.xpath('.//div[@class="elRowTitle"]/p[contains(text(),"JAN")]/'
                               'ancestor::li/div[@class="elRowData"]/p/text()').get(),
            url=response.request.url
        )

    # 楽天商品ページのパーサー
    def rakuten_parse_item(self, response):
        # priceをint型に変換
        try:
            price_str = response.xpath('.//div[@id="priceCalculationConfig"]/@data-price').get()
            if isinstance(price_str, str):
                int_price = int(price_str)
            else:
                int_price = price_str
        except:
            print('価格情報が取得できません')
            int_price = None
        # Items.pyのPostItemへyieldする
        yield PostItem(
            title=response.xpath('.//span[@class="item_name"]/b/text()').get(),
            price=int_price,
            jan=response.xpath('.//input[@id="ratRanCode"]/@value').get(),
            url=response.request.url
        )

    #
    # def parse(self, response):
    #     # maxpageを超えないようにするためのページのカウンター設定
    #     self.page_counter += 1
    #     # 商品の要素を取得
    #     # inspect_response(response, self)
    #     elems = response.xpath('//div[@class="elName"]')
    #     for elem in elems:
    #         yield response.follow(url=elem.xpath('.//a/@href').get(),
    #                               callback=self.parse_item)
    #     # 次のページのリンクを取得
    #     next_page = response.xpath('//li[@class="elNext"]/a/@href').get()
    #
    #     # 次のページがあれば繰り返し
    #     if next_page and self.page_counter <= int(self.maxpage):
    #         yield response.follow(url=next_page, callback=self.parse)
    #
    # # 商品ページのパーサー
    # def parse_item(self, response):
    #     # priceのカンマを削除してint型に変換
    #     before_price = response.xpath('.//span[@class="elPriceNumber"]/text()').get()
    #     int_price = int(before_price.replace(',', ''))
    #     # Items.pyのPostItemへyieldする
    #     yield PostItem(
    #         title=response.xpath('.//p[@class="elName"]/text()').get(),
    #         price=int_price,
    #         jan=response.xpath('.//div[@class="elRowTitle"]/p[contains(text(),"JAN")]/'
    #                            'ancestor::li/div[@class="elRowData"]/p/text()').get(),
    #         url=response.request.url
    #     )
    #

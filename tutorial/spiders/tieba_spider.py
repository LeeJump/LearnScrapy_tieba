import scrapy
from scrapy.loader import ItemLoader
from ..items import postItem
from scrapy.contrib.loader.processor import TakeFirst, MapCompose, Join


class DefaultItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


class x_path():
    def __init__(self):
        self.title = ".//a[contains(@class,'j_th_tit')]/text()"
        self.reply = ".//span[@title='回复']/text()"
        self.abstract = ".//div[contains(@class,'threadlist_abs')]/text()"
        self.author = ".//span[@class='frs-author-name-wrap']//a/text()"
        self.last_replyer = ".//span[contains(@class,'j_replyer')]//a/text()"

    def __str__(self):
        return 'i am a class of xpath'


class DmozSpider(scrapy.Spider):
    name = "tieba"
    allowed_domains = ["tieba.baidu.com"]
    start_urls = []
    main_url = "http://tieba.baidu.com/f?kw=%E6%B9%96%E5%8C%97%E7%AC%AC%E4%BA%8C%E5%B8%88%E8%8C%83%E5%AD%A6%E9%99%A2&ie=utf-8&pn="
    xp = x_path()
    base_xpath = "/html//ul[@id='thread_list']/li[contains(@class,'j_thread_list')]"
    for x in range(2000):
        start_urls.append(main_url + str(x * 50))

    def parse(self, response):
        for post in response.xpath(self.base_xpath):
            i = DefaultItemLoader(item=postItem(), selector=post)
            i.add_xpath('title', self.xp.title)
            i.add_xpath('replys', self.xp.reply)
            i.add_xpath('abstract', self.xp.abstract)
            i.add_xpath('author', self.xp.author)
            i.add_xpath('last_replyer', self.xp.last_replyer)
            yield i.load_item()


'''
            item = postItem()
            item['title'] = post.xpath(".//a[contains(@class,'j_th_tit')]/text()").extract_first()
            item['replys'] = post.xpath(".//span[@title='回复']/text()").extract_first()
            # .replace("\n",'').strip()
            item['abstract'] = post.xpath(".//div[contains(@class,'threadlist_abs')]/text()").extract_first().replace("\n", '').strip()
            item['author'] = post.xpath(".//span[@class='frs-author-name-wrap']//a/text()").extract_first()
            item['last_replyer'] = post.xpath(".//span[contains(@class,'j_replyer')]//a/text()").extract_first()
            yield item
'''

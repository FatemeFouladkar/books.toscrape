import scrapy
import datetime

class BooksSpider(scrapy.Spider):
    name = 'books'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']

    custom_settings = {
        'FEED_URI': f'output/books_{datetime.datetime.today().strftime("%Y-%M-%d")}.csv',
        'FEED_FORMAT': 'csv',
        'FEED_EXPORTERS': {'csv': 'scrapy.exporters.CsvItemExporter'},
        'FEED_EXPORT_ENCODING': 'utf-8',
        'FEED_EXPORT_FIELDS': ('title', 'price', 'rating') 
    }

    def parse(self, response):
        for book in response.xpath("//article[@class='product_pod']"):
            yield {
                'title' : book.xpath(".//h3/a/text()").get(),
                'price' : book.xpath(".//p[@class='price_color']/text()").get(),
                'rating' : book.xpath(".//p[contains(@class,'star-rating')]/@class").get().split(' ')[-1],
                }

        next_page = response.xpath("//li[@class='next']/a/@href").get()
        if next_page:
            yield response.follow(next_page)

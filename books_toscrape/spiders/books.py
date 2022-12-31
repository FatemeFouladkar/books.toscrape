import scrapy


class BooksSpider(scrapy.Spider):
    name = 'books'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']

    def parse(self, response):
        for book in response.xpath("//article[@class='product_pod']"):
            yield {
                'title' : book.xpath(".//h3/a/text()").get(),
                'price' : book.xpath(".//p[@class='price_color']/text()").get(),
                'rating' : book.xpath(".//p[contains(@class,'star-rating')]/@class").get().split(' ')[-1],
                }

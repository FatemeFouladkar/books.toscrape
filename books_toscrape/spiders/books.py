import scrapy
import datetime

class BooksSpider(scrapy.Spider):
    name = 'books'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']

    custom_settings = {
        'CONCURRENT_REQUESTS': 10,
        'DOWNLOAD_DELAY': 0.1,
        'FEED_URI': f'output/books_{datetime.datetime.today().strftime("%Y-%m-%d")}.csv',
        'FEED_FORMAT': 'csv',
        'FEED_EXPORTERS': {'csv': 'scrapy.exporters.CsvItemExporter'},
        'FEED_EXPORT_ENCODING': 'utf-8',
        'FEED_EXPORT_FIELDS': ('product_type','title','price_excl_tax',\
                                'price_incl_tax','tax','rating','availability',\
                                'description','upc','reviews') 
    }

    def parse(self, response):
        for book in response.xpath("//article[@class='product_pod']"):
            yield response.follow(book.xpath(".//h3/a/@href").get(), callback=self.parse_book)

        next_page = response.xpath("//li[@class='next']/a/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_book(self, response):
        yield {
            'product_type': response.xpath("//table[@class='table table-striped']/tr[th/text()='Product Type']/td/text()").get(),
            'title': response.xpath("//div[@class='col-sm-6 product_main']/h1/text()").get(),
            'price_excl_tax': response.xpath("//table[@class='table table-striped']/tr[th/text()='Price (excl. tax)']/td/text()").get(),
            'price_incl_tax': response.xpath("//table[@class='table table-striped']/tr[th/text()='Price (incl. tax)']/td/text()").get(),
            'tax': response.xpath("//table[@class='table table-striped']/tr[th/text()='Tax']/td/text()").get(),
            'rating': response.xpath("//p[contains(@class,'star-rating')]/@class").get().split(' ')[-1],
            'availability': response.xpath("//table[@class='table table-striped']/tr[th/text()='Availability']/td/text()").get(),
            'description': response.xpath("//div[@id='product_description']/following::p/text()").get(),
            'upc': response.xpath("//table[@class='table table-striped']/tr[th/text()='UPC']/td/text()").get(),
            'reviews': response.xpath("//table[@class='table table-striped']/tr[th/text()='Number of reviews']/td/text()").get(),
        } 
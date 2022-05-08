import scrapy
from scrapy_splash import SplashRequest

from scrapySplash.items import BookItem

script = """
function main(splash, args)
  assert(splash:go(args.url))
  assert(splash:wait(5))
  return {
    html = splash:html(),
    png = splash:png(),
    har = splash:har(),
  }
end
"""


class BookSpider(scrapy.Spider):
    name = 'book'
    allowed_domains = ['spa5.scrape.center']
    base_url = 'https://spa5.scrape.center'

    http_user = 'admin'
    http_pass = 'admin'

    def start_requests(self):
        """
        开始请求
        :return:
        """
        start_url = f'{self.base_url}/page/1'
        yield SplashRequest(start_url, callback=self.parse_index, args={'lua_source': script}, endpoint='execute')

    def parse_index(self, response):
        """
        解析首页
        :param response:
        :return:
        """
        items = response.css('.item')
        for item in items:
            href = item.css('.top a::attr(href)').extract_first()
            detail_url = response.urljoin(href)
            # yield Request(detail_url, callback=self.parse_detail)
            # use SplashRequest
            yield SplashRequest(detail_url, callback=self.parse_detail, priority=2, args={'lua_source': script},
                                endpoint='execute')

    def parse_detail(self, response):
        """
        解析详情页
        :param response:
        :return:
        """
        name = response.css('.name::text').extract_first()
        tags = response.css('.tags button span::text').extract()
        score = response.css('.score::text').extract_first()
        price = response.css('.price span::text').extract_first()
        cover = response.css('.cover::attr(src)').extract_first()
        tags = [tags.strip() for tags in tags] if tags else []
        score = score.strip() if score else ''
        item = BookItem(name=name, tags=tags, score=score, price=price, cover=cover)
        yield item


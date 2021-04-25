import scrapy


class OtodomTableSpider(scrapy.Spider):
    name = 'otodom_table'
    allowed_domains = ['www.otodom.pl']
    start_urls = ['https://www.otodom.pl/sprzedaz/mieszkanie/mazowieckie/?search%5Bregion_id%5D=7']

    def parse(self, response):
        """
        Links list parser
        :param response: system link
        :return: None
        """
        # list of links
        apt_list = list(set(response.xpath("//a[@data-featured-name='listing_no_promo']/@href").extract() +
                            response.xpath("//a[@data-featured-name='promo_top_ads']/@href").extract()))

        # yields parsed item due to the link
        yield from response.follow_all(apt_list, self.parse_item)

        # works with pagination
        # next page link
        next_page = response.xpath("//li[@class='pager-next']//a/@href").extract_first()

        # if next page exists
        if next_page:
            yield scrapy.Request(
                response.urljoin(next_page),
                callback=self.parse)

    def parse_item(self, response):
        """
        Item parser, uses previously parsed link to an item
        :param response: system link
        :return: None
        """

        # items in the table title - value
        names = response.xpath("//div[@class='css-o4i8bk ev4i3ak2']/@title").extract()
        values = response.xpath("//div[@class='css-1ytkscc ev4i3ak0']/@title").extract()

        # dictionary which represents result
        res = {n: v for n, v in zip(names, values)}

        # other parameters which should be parsed
        for name, xpath in zip(['title', 'address', 'Cena', 'Cena za metr kwadratowy'],
                               ["//h1[@data-cy='adPageAdTitle']/text()",
                                "//a[@class='css-1qz7z11 e1nbpvi61']/text()",
                                "//strong[@aria-label='Cena']/text()",
                                "//div[@aria-label='Cena za metr kwadratowy']/text()"]):
            content = response.xpath(xpath).extract()
            if content:
                res.update({name: content})

        # yields results
        yield res

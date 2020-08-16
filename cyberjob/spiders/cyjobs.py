import scrapy


class CyjobsSpider(scrapy.Spider):
    name = "cyjobs"

    def start_requests(self):
        urls = ['https://crowdworks.jp/public/jobs?category=jobs&order=score']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        #JOB_SELECTOR = '.item_title'
        JOB_SELECTOR = '.item'
        #JOB_SELECTOR = '.job_data_row'
        for cyjob in response.css(JOB_SELECTOR):

            JOBNO_SELECTOR = 'a ::attr(href)'
            TITLE_SELECTOR = 'a ::text'
            DESC_SELECTOR = 'p ::text'
            yield {
                'link': 'https://crowdworks.jp' + cyjob.css(JOBNO_SELECTOR).extract_first(),
                'title': cyjob.css(TITLE_SELECTOR).extract_first(),
                'description': cyjob.css(DESC_SELECTOR).extract_first(),
            }

        NEXT_PAGE_SELECTOR = '.to_next_page ::attr(href)'
        next_page = response.css(NEXT_PAGE_SELECTOR).extract_first()
        if next_page:
            yield scrapy.Request(
                response.urljoin(next_page),
                callback=self.parse
            )

        #page = response.url.split("/")[-2]
        #filename = 'crowdworks-%s.html' % page
        #with open(filename, 'wb') as f:
        #    f.write(response.body)
        #self.log('Saved file %s' % filename)
import scrapy



class InformaticsCoursesSpider(scrapy.Spider):
    name = "informatics"
    start_urls = [
        'https://course.inf.ed.ac.uk/',
    ]

    def parse(self, response):
        titles_raw = response.css('#content > div > table > thead > tr > th')
        courses_raw = response.css('#content > div > table > tbody > tr')

        # Scrape the first row (titles of each row)
        titles = list(titles_raw.css('th::text').extract())

        # Go through every row / course
        for course_raw in courses_raw:
            # single course will contain data regarding one course
            single_course = {}
            for i, info in enumerate(course_raw.xpath('./td')):
                # TABLE being parse
                #  ------------------------------------------------------------------------------
                # | Course URL         | EUCLID Code | Acronym | AI | GC | CS | SE | Level | ... | - TITLES
                #  ------------------------------------------------------------------------------
                # | Advanced Databases | INFR11011   | ADBS    |    |    | CS |    | 10    | ... | - COURSE
                # ...

                # First column is course name, but it's called Course URL, gonna rename to courseName
                # Second column is both EUCLID Code and Course URL, thus gonna use Course URL form it
                # Other items will contain correct data
                if i == 0:
                    single_course['courseName'] = info.css('::text').extract_first()
                else:
                    single_course[titles[i]] = info.css('::text').extract_first()

                    if i == 1:
                        drps_page = info.css('a').xpath('@href').extract_first()
                        single_course[titles[0]] = drps_page

                        if drps_page:
                            request = response.follow(drps_page, self.parse_drps)
                            request.meta['course'] = single_course
                            yield request

    def extract_td_text(self, node):
        return '\n'.join([text.extract() for text in node.css('td::text')]).strip()

    def parse_drps(self, response):
        inf = response.css('body > table.content > tr > td > table > tr > td')
        single_course = response.meta['course']

        for i, c in enumerate(inf):
            cell_name = self.extract_td_text(c)

            if cell_name == 'Summary':
                single_course['Summary'] = self.extract_td_text(inf[i + 1])
            elif cell_name == 'Course description':
                single_course['Description'] = self.extract_td_text(inf[i + 1])

        yield single_course


# 'courseName' : info.css('a::text').extract_first(),
# 'courseURL' : info.css('a').xpath('@href').extract_first(),
# 'courseCode' : info.css('a::text').extract_first(),
# 'codeURL' : info.css('a').xpath('@href').extract_first(),
# 'acronym' : info.css('td::text').extract_first(),
# 'ai' : info.css('td::text').extract_first(),
# 'cg' : info.css('td::text').extract_first(),
# 'cs' : info.css('td::text').extract_first(),
# 'se' : info.css('td::text').extract_first(),
# 'level': info.css('td::text').extract_first(),
# 'points' : info.css('td::text').extract_first(),
# 'year' : info.css('td::text').extract_first(),
# 'delivery' : info.css('td::text').extract_first(),
# 'examDiet' : info.css('td::text').extract_first(),
# 'workExamRatio' : info.css('td::text').extract_first(),
# 'lecturerCoordinator' : info.css('a::text').extract_first()





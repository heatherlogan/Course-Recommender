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
                # The first item will contain both course name and href while
                # other items will contain only text
                if i == 0:
                    single_course['courseName'] = info.css('::text').extract_first()
                elif i == 1:
                    single_course[titles[0]] = info.css('a').xpath('@href').extract_first()
                    single_course[titles[1]] = info.css('::text').extract_first()
                else:
                    single_course[titles[i]] = info.css('::text').extract_first()

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
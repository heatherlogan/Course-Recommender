INSTRUCTIONS:

This web scraper uses 'Scrapy' Library. Please refer to it's website to understand how it works/how to install

To run this scraper for the root website: 'https://course.inf.ed.ac.uk/' go to directory '/scraper/'

On terminal, type in:

scrapy crawl informatics 


To create the json file, on terminal type:

scrapy crawl informatics -o 'filename'.json


(Replace 'filename' with whatever name you wish to call the json file.)


'pdftotext' library was used to scrape pdf files. To get pdftotext, ensure you have gcc installed. If not, on command line:

brew install gcc
brew install plopper
pip install pdftotext


To run the scraper for PDF file which contains the course averages, 'course_result_summary.pdf' 

On terminal:

python parse_average.py 

This will print out the parsed pdf file. (@vik will format it all nice and neat)
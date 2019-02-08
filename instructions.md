# About

This document contains instructions to run the scraping files (courses, feedback and such) as well as the script for creating the final course data containing .json file. They correspond to content found in 'course_scraping' folder, 'website' folder stores all the files used to build https://inf-search.appspot.com; and 'website/requirements.txt' shows the needed packages. 

NOTE: The files mentioned below were created using Python3.7 and should be run using this version, all the external libraries used are also assumed for Python3.7

## Web Scraper
The web scraper uses 'Scrapy' Library to retrieve informatics course information. Install using:
> pip install Scrapy

The official documentation and how 'Scrapy' works can be found in https://scrapy.org/

## Running the web scraper
To run the scraper, first go to directory 'course_scraping/scraper/', then, using terminal, type in:
> scrapy crawl informatics -o informatics.json
This will crawl the informatics website(https://course.inf.ed.ac.uk/) and store the collected data inside informatics.json file. 

## PDF Scraper
To scrape the PDF files, we used 'pdftotext' and 'pdfminer' libraries, as well as BeautifulSoup4.* The produced files are 'feedback.json' and 'average.txt' respectively. 

These files are all ready to use and we have also prepared a file 'labels.txt'. This includes every course labelled with an appropriate area of interest. It was done manually and would need to be maintained by an administration or someone looking after the system. To combine all these files make sure you are in 'course_scraping/' folder and run:
> python course_builder.py

This will produce an output 'course_data.json' which is being used by the recommender and the search engine. It combines all previously mentioned files into one place to have a full representation of each course. The file can be found in 'website/json_files/' which is the folder used by the search and recommender engines.


\* To get pdftotext, ensure you have gcc installed. If not, on command line:

> brew install gcc
> brew install plopper
> pip install pdftotext

Pdfminer is more straighforward:
> pip install pdfminer3k

Same follows for remaining libraries:
> pip install bs4
> pip install textblob 
> pip install requests


To run the scraper for average score PDF file, 'course_result_summary.pdf', make sure you are in 'course_scraping/' folder and on terminal type:
> python parse_average.py 

It will produce 'average.txt' file.

To run the scraper for the feedback PDF file, as well as to evaluate it for polarity and subjectivity, make sure you are in 'course_scraping/' folder and run:
> python pdf-downloader.py
> python TextBlob_analysis.py
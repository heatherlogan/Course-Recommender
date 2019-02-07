NOTE: The files were created using Python 3.7 and should be run using this version

## Libraries
The web scraper uses 'Scrapy' Library. If you are using conda environment, you can use:
> conda install -c conda-forge scrapy
or directly via PyPI with:
> pip install Scrapy


## Running the scraper

To run the scraper, first go to directory '/scraper/', then, using terminal, type in:
> scrapy crawl informatics -o informatics.json
This will crawl the informatics website('https://course.inf.ed.ac.uk/') and store the collected data inside informatics.json file. 


## PDFs

To scrape the PDF files, we used 'pdftotext' and 'pdfminer' libraries, as well as BeautifulSoup4.* The produced files are 'feedback.json' and 'average.txt' respectively. 

These files are all ready to use and we have also prepared a file 'labels.txt'. This includes every course labelled with an appropriate area of interest. It was done manually and would need to be maintained by an administration or someone looking after the system. To combine all these files, run:
> python course_builder.py

This will produce an output 'course_data.json' which is being used by the recommender and the search engine. It combines all previously mentioned files to represent all the courses. 

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


To run the scraper for average score PDF file, 'course_result_summary.pdf', on terminal:
> python parse_average.py 

It will produce 'average.txt' file.

To run the scraper for the feedback PDF file, as well as to get the 
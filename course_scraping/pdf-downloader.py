# for scrap url
import requests
import re
#import os
from bs4 import BeautifulSoup  #please install bs4
import json
# for pdf processing
from urllib.request import urlopen
from pdfminer.pdfinterp import PDFResourceManager, process_pdf #please install pdfminer3k
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from io import StringIO
from io import open


def GetPage(url):
    page = requests.get(url)
    html = page.text
    return html

def GetList(html):
    soup = BeautifulSoup(html, "html.parser")
    list = soup.find_all(href=re.compile("2017-2018/"))
    pdfs = []
    for li in list:
        if (li.get('href'))[-4:] == ".pdf":
            pdfs.append(li.get('href'))
    return pdfs

'''def DownloadPdf(pdf):
    path = "C:/Users/LOU MING/Desktop/gp_ttds/pdf/" + pdf[67:]   # need to be changed for different machine
    urls = pdf
    r = requests.get(urls)
    f = open(path, "wb")
    f.write(r.content)
    f.close()
    return urls'''

def readPDF(pdfFile):      # input pdf url, output a string of all the content
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)

    process_pdf(rsrcmgr, device, pdfFile)
    device.close()

    content = retstr.getvalue()
    retstr.close()
    return content

def feedback_processing(String_content):    # input: a string of scraped content, output: a list of feedback
    flag = 0  # flag = 1 if current line is comment
    feedback = []
    for line in String_content.splitlines():
        word_type = line.split()
        # print(word_type)
        if len(word_type) != 0 and len(word_type) != 1 and word_type[0] == '\uf0a7':  # if the sentence starts with '\uf0a7' and sth behind, it is a comment
            flag = 1
            feedback.append(' '.join(word_type[1:]))
        elif len(word_type) != 0 and flag == 1:  # deal with the situation of second-line comment
            flag = 0
            feedback[-1] = ' '.join(word_type) + feedback[-1]
        else:
            flag = 0
    # print(feedback)
    return feedback


url = "https://www.inf.ed.ac.uk/admin/ITO/course-survey-reports/"
# root_url = ""
#print(GetList(GetPage(url)))
pdfs = GetList(GetPage(url))
Output = [] # outputed json file
for pdf in pdfs:
    #print("Download finished: "+DownloadPdf(pdf))  # used to be DownloadPdf(pdf, root_url)
    pdfFile = urlopen(pdf)   # open url
    outputString = readPDF(pdfFile) # get pdf content
    feedback = feedback_processing(outputString) # change pdf content to a list of feedback
    code = pdf[67:-4]    # course code
    code_feedback = {code: feedback}
    Output.append(code_feedback)
    pdfFile.close()
with open('feedback.json', 'w', encoding='utf-8') as outfile:
    json.dump(Output, outfile, sort_keys=True, indent=4, ensure_ascii=False)

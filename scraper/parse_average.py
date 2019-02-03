import pdftotext
import re

def main():
    # Load your PDF
    with open("course_result_summary.pdf", "rb") as f:
        pdf = pdftotext.PDF(f)

    all_text = "\n".join(pdf).strip()
    split_by_line = all_text.split('\n')
    print [re.split(r'\s{2,}', x) for x in split_by_line]

    
if __name__ == '__main__':
    main()
import pdftotext
import re

def main():
    # Load your PDF
    with open("course_result_summary.pdf", "rb") as f:
        pdf = pdftotext.PDF(f)

    all_text = "".join(pdf).strip()
    #print(all_text)
    split_by_line = all_text.split('\n')
    #print(split_by_line)

    # for s in split_by_line:
    #     print(s)
    course =  [re.split(r'\s{1,}', x) for x in split_by_line]

    for c in course:
        if c[0].startswith('INF'):
            print(c[0], c[-2])

    with open('../average.txt', 'w') as f:
        f.write('INFCODE\t' + 'AVERAGE\n')

        for c in course:
            if c[0].startswith('INF'):
                f.write(c[0] + '\t' + c[-2] + '\n')


if __name__ == '__main__':
    main()
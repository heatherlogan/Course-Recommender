from textblob import TextBlob
import json

# function to calculate polarity and subjectivity
def pola_subj(text):   # input: text output: polarity and subjectivity
    #text_temp = TextBlob(text).correct() # correct misspelling
    pola = TextBlob(text).sentiment.polarity
    subj = TextBlob(text).sentiment.subjectivity
    pola_subj_tuple = (pola, subj)
    return pola_subj_tuple

# read feedback.json file and store all the corresponding data
with open('feedback.json', encoding='utf-8-sig') as json_file:
    json_feedback = json.load(json_file)  # a list of data: [course code: feedbacks]
Output = []
for each_course in json_feedback:
    for course_code, feedbacks in each_course.items(): # this loop will only be excuted once
        sum_pola = 0
        sum_subj = 0
        for each_feedback in feedbacks:
            pola_subj_temp = pola_subj(each_feedback)
            sum_pola = sum_pola + pola_subj_temp[0]
            sum_subj = sum_subj + pola_subj_temp[1]
        if feedbacks:
            average_pola = sum_pola/len(feedbacks)
            average_subj = sum_subj/len(feedbacks)
            output = {'course_code': course_code, 'polarity': average_pola, 'subjectivity': average_subj}
            Output.append(output)
# store data to json file
with open('course_evaluation.json', 'w', encoding='utf-8') as outfile:
    json.dump(Output, outfile, sort_keys=True, indent=4, ensure_ascii=False)
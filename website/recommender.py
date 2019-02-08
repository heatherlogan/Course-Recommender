import re
import pandas
import json
import numpy as np
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

stopWords = set(stopwords.words('english'))

def preprocess_series(series):
    pp_text = []

    def preprocess(text):
        text = re.sub(r'([^\s\w]|_)+', '', text)
        preprocessed = []
        text = word_tokenize(text)
        for word in text:
            word = word.lower()
            if word not in stopWords:
                preprocessed.append(word)
        return preprocessed

    for desc in series:
        desc = preprocess(desc)
        pp_text.append(' '.join(desc))

    new_series = pandas.Series(pp_text)

    return new_series

def level_allowed(int):

    # course levels you can take by year

    levels = {2: ['8'], 3: ['9', '10'], 4: ['10', '11'], 5: ['11'] }
    return levels[int]


def TFIDF(df):

    # returns full similarity matrix (all courses x all courses)

    df['Course Description'] = df['Summary'] + df['Course Description']
    df['Course Description'] = preprocess_series(df['Course Description'])

    tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 2), min_df=0, stop_words='english')
    tfidf_matrix = tf.fit_transform((df['Summary']))
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

    return cosine_sim


def get_recommendations(df, list):

    # sorting similarity matrix by largest similarity

    sim_scores = list
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[0:]
    course_indices = [i[0] for i in sim_scores]
    return df.iloc[course_indices]


class Recommendation:

    def __init__(self, num, code, name, summary, average, area, acronym, level, credits, delivery, examdiet, cwexam,
                 coordinator, feedback, url):
        self.num = num
        self.code = code
        self.name = name
        self.summary = summary
        self.average = average
        self.area = area
        self.acronym = acronym
        self.level = level
        self.credits = credits
        self.delivery = delivery
        self.examdiet = examdiet
        self.cwexam = cwexam
        self.coordinator = coordinator
        self.feedback = feedback
        self.url = url

def reccomendation_object(num, df, index):
    record = df.iloc[index]
    code = record['Code']
    reccom = Recommendation(num, record["Code"], record['Name'], record['Summary'],
                            record['Average'], record['Area'], record['Acronym'],
                            record['Level'], record['Credits'], record['Delivery'], record['Exam Diet'],
                            record['Coursework/Exam'], record['Coordinator'],
                            record['Feedback'], record['Link'])
    return reccom


def match_prerequisites(df, indices_name, list):

    # gets prereq course id by name

    id_list = []
    for l in list:
        try:
            id = df.iloc[indices_name[l]]['Code']
            id_list.append(id)
        except KeyError:
            pass

    return id_list


def normalize_enjoyment(dictionary):

    # normalizes enjoyment rating so it doesnt weight scores too much

    s = sum(dictionary.values())

    new_vals = {}
    for k, v in dictionary.items():
        new_vals[k] = 1 + v/s

    return new_vals





def all_reccomendations(previous_courses, year_of_study, interests):

    with open('json_files/course_data.json', 'r') as f:
        data = json.load(f)

    df = pandas.DataFrame(data['courses'])

    # similariy matrix
    cosine_sim = TFIDF(df)
    courses = df['Name']
    indices = pandas.Series(df.index, index=df['Code'])
    indices_name = pandas.Series(df.index, index=df['Name'])

    array = []

    print("Course + Rating")

    # loop through user input courses

    for course_code, enjoyment in previous_courses.items():

        # get similarity vector for each course against other courses

        idx = indices[course_code]
        raw_scores = cosine_sim[idx]
        modified = []
        mean_raw = sum(raw_scores)/float(len(raw_scores))

        print("\t", df.iloc[indices[course_code]]['Name'], enjoyment)

        for i, score in enumerate(raw_scores):

            # for each score, filter out (set =0) if the corresponding course is not a valid option
            record = df.iloc[i]
            if record['Code'] in previous_courses or record['Level'] \
                    not in level_allowed(year_of_study):
                new_score = 0
            if "Distance Learning" in record['Name']:
                new_score = 0
            else:
                # weight score by the enjoyment of the course. Add small weight for average grade.
                new_score = (enjoyment * score)
                # if course area is in user inputted interests, add a weight

                if record['Area'] in interests:
                    newscore = new_score * 2

            modified.append(new_score)

        array.append(modified)

    # get recommnedations with weighted similarities

    array = np.array(array)
    new_reccomend = ([sum([row[i] for row in array]) for i in range(0,len(array[0]))])
    tuple_list = [(i, score) for i, score in enumerate(new_reccomend) if score != 0]

    reccoms = get_recommendations(df, tuple_list)[:6]

    output_reccoms = []

    for i, r in enumerate(reccoms['Code']):
        obj = reccomendation_object(i+1, df, indices[r])
        if obj.code not in previous_courses.keys():

            output_reccoms.append(obj)

    return output_reccoms


def course_obj_byname(matches, data, name):

    df = pandas.DataFrame(data['courses'])
    indices_name = pandas.Series(df.index, index=df['Name'])
    obj = reccomendation_object(matches, df, indices_name[name])

    return obj

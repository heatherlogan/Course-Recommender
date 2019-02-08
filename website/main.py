import json
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from flask_wtf.csrf import CSRFProtect
from nltk.stem.porter import *

from recommender_forms import Courses_Form
from recommender import all_reccomendations, course_obj_byname

app = Flask(__name__)
Bootstrap(app)
csrf = CSRFProtect()
csrf.init_app(app)

# app.run(port = 8080)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


# Home page
@app.route('/')
def hello():
    return render_template("index.html")


@csrf.exempt
@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'GET':
        return render_template('search.html')

    if request.method == 'POST':
        stemmer = PorterStemmer()
        courses = {}
        text = request.form['text']
        text = text.lower()
        text = stemmer.stem(text)
        text = text.split()

        textSend = "The output for your search was: \n"

        with open('json_files/course_data.json') as json_file:
            data = json.load(json_file)
            for p in data['courses']:
                wordlist = []
                for word in p['Name'].split() + p['Area'].split():
                    word = word.lower()
                    word = stemmer.stem(word)
                    wordlist.append(word)
                courses[p['Name']] = wordlist

            stemmed = []
            for word in range(0, len(text)):
                if (text[word] in ['1', '2', '3', '4', '5']):
                    if (word > 0):
                        if (text[word - 1] == "year"):
                            stemmed[len(stemmed) - 1] = "year" + text[word]
                        else:
                            stemmed.append(stemmer.stem(text[word]))
                    else:
                        stemmed.append(stemmer.stem(text[word]))
                else:
                    stemmed.append(stemmer.stem(text[word]))

            search = stemmed

            results = {}

            for course in courses:
                matches = 0
                for words in range(0, len(courses[course])):
                    for query in range(0, len(search)):
                        if search[query] in courses[course][words]:
                            if (query < len(search) - 1 and words < len(courses[course]) - 1):
                                if (search[query + 1] in courses[course][words + 1]):
                                    matches += 1
                                if (search[query + 1] == courses[course][words + 1]):
                                    matches += 1
                            matches += 1

                        if (search[query] == courses[course][words]):
                            if (query < len(search) - 1 and words < len(courses[course]) - 1):
                                if (search[query + 1] in courses[course][words + 1]):
                                    matches += 1
                                if (search[query + 1] == courses[course][words + 1]):
                                    matches += 1
                            matches += 1

                if (matches > 0):
                    if matches not in results:
                        results[matches] = []
                    results[matches].append(course)

            output_objs = []

            for output in reversed(sorted(results.keys())):
                for course in results[output]:
                    obj = course_obj_byname(str(output), data, course)
                    output_objs.append(obj)

                    textSend = textSend + course + " Matches: " + str(output) + "\n"

            textSend = textSend.split('\n')

        return render_template('search.html', text=textSend, objs=output_objs)


@app.route('/recommend', methods=['GET', 'POST'])
def recommend():
    form = Courses_Form()

    with open('json_files/course_data.json', 'r') as f:
        data = json.load(f)

    courses = sorted(data['courses'], key=lambda course: course['Name'])
    interest_list = sorted(list(set([course['Area'] for course in data['courses']])))
    years = ['3', '4', '5']
    scores = ["1", "2", "3", "4", "5"]

    if request.method == 'GET':
        return render_template('recommender.html', courses=courses, form=form, scores=scores, interests=interest_list,
                               years=years)

    if request.method == "POST":
        taken_courses = {}

        course1 = request.form['course_1']
        course2 = request.form['course_2']
        course3 = request.form['course_3']
        course4 = request.form['course_4']
        course5 = request.form['course_5']
        course1_score = request.form['course_1_score']
        course2_score = request.form['course_2_score']
        course3_score = request.form['course_3_score']
        course4_score = request.form['course_4_score']
        course5_score = request.form['course_5_score']
        taken_courses[course1] = course1_score
        taken_courses[course2] = course2_score
        taken_courses[course3] = course3_score
        taken_courses[course4] = course4_score
        taken_courses[course5] = course5_score
        year_of_study = request.form['yr']
        interest1 = request.form['interest_1']
        interest2 = request.form['interest_2']
        interest3 = request.form['interest_3']

        interests = interest1 + interest2 + interest3

        taken_courses_fixed = {}
        for course, score in taken_courses.items():
            if len(course) > 0 and score != '-':
                taken_courses_fixed[course] = int(score)

        output = all_reccomendations(taken_courses_fixed, int(year_of_study), interests)

    return render_template('recommender.html', courses=courses, form=form, scores=scores,
                           interests=interest_list, years=years, recommendations=output)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
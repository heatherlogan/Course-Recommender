import os.path
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import json
from flask_wtf import FlaskForm


class Courses_Form(FlaskForm):

    with open('json_files/course_data.json', 'r') as f:
        data = json.load(f)












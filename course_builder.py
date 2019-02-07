import sys
import json

keys = {1:'courseName', 2:'EUCLID Code', 3:'Course URL', 4:'Acronym', 5:'Level', 6:'Points', 
    7:'Year', 8:'Delivery', 9:'Exam Diet', 10:'Work%/Exam%', 11:'Lecturer(s)/Coordinator(s)', 
    12:'Summary', 13:'Description',  99:['AI', 'CG', 'CS', 'SE'], }

def main():
    informatics_file = './scraper/informatics.json'
    with open(informatics_file) as f:
        courses = json.load(f)

    feedback_file = 'feedback.json'
    with open(feedback_file) as f:
        feedback = json.load(f)
    
    average_file = 'average.txt'
    with open(average_file) as f:
        avgs = f.read().strip().split('\n')
    avgs = avgs[1:]

    labels_file = 'labels.txt'
    with open(labels_file) as f:
        labels = f.read().strip().split('\n')
    
 
    inf_codes = dict()
    course_dict = {'courses':[]}
    for i, course in enumerate(courses):
        temp_dict = dict()
        temp_dict['Name'] = course[keys[1]]  
        temp_dict['Code'] = course[keys[2]]   
        temp_dict['Link'] = course[keys[3]]   
        temp_dict['Acronym'] = course[keys[4]]  
        temp_dict['Level'] = course[keys[5]]  
        temp_dict['Credits'] = course[keys[6]]   
        temp_dict['Year'] = course[keys[7]] 
        temp_dict['Delivery'] = course[keys[8]] 
        if course[keys[9]]:
            temp_dict['Exam Diet'] = course[keys[9]] 
        else:
            temp_dict['Exam Diet'] = "Not Available"
        temp_dict['Coursework/Exam'] = course[keys[10]]  
        temp_dict['Coordinator'] = course[keys[11]] 
        temp_dict['Summary'] = course[keys[12]]
        temp_dict['Course Description'] =  course[keys[13]] 
        temp_dict['Average'] = "Not Available"
        temp_dict['Feedback'] = "Not Available"
        temp_dict['Area'] = "Not Available"

        inf_codes[temp_dict['Code']] = i
        course_dict['courses'].append(temp_dict)
    
    for feed in feedback:
        key_to_chek = list(feed.keys())[0]
        if key_to_chek in inf_codes.keys():
           num = inf_codes[key_to_chek]
           course_dict['courses'][num]['Feedback'] = feed[key_to_chek]


    for avg in avgs:
        key_to_chek, score = avg.split()       
        if key_to_chek in inf_codes.keys():
           num = inf_codes[key_to_chek]
           course_dict['courses'][num]['Average'] = score

    for label in labels:
        key_to_chek, label = label.split('\t') 
        if key_to_chek in inf_codes.keys():
           num = inf_codes[key_to_chek]
           course_dict['courses'][num]['Area'] = label

    # print all data in pretty .json format
    with open('course_data.json', 'w') as fp:
        json.dump(course_dict, fp, indent=4)
    
              
if __name__ == '__main__':
    main()
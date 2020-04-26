from flask import Flask, escape, request, jsonify, abort, make_response
import copy
import sqlite3
import json
from marshmallow import Schema, fields, ValidationError


# with open ("answer_key_schema.json", 'r') as f:
#     test_schema = json.load(f)

class ActualExpectedSelectionSchema(Schema):
    actual       = fields.Str()
    expected     = fields.Str()

class SubmissionResultsSchema(Schema):
    Q1           = fields.Nested(ActualExpectedSelectionSchema)
    Q2           = fields.Nested(ActualExpectedSelectionSchema)
    Q3           = fields.Nested(ActualExpectedSelectionSchema)
    Q4           = fields.Nested(ActualExpectedSelectionSchema)
    Q5           = fields.Nested(ActualExpectedSelectionSchema)
    Q6           = fields.Nested(ActualExpectedSelectionSchema)
    Q7           = fields.Nested(ActualExpectedSelectionSchema)
    Q8           = fields.Nested(ActualExpectedSelectionSchema)
    Q9           = fields.Nested(ActualExpectedSelectionSchema)
    Q10          = fields.Nested(ActualExpectedSelectionSchema)
    Q11          = fields.Nested(ActualExpectedSelectionSchema)
    Q12          = fields.Nested(ActualExpectedSelectionSchema)
    Q13          = fields.Nested(ActualExpectedSelectionSchema)
    Q14          = fields.Nested(ActualExpectedSelectionSchema)
    Q15          = fields.Nested(ActualExpectedSelectionSchema)
    Q16          = fields.Nested(ActualExpectedSelectionSchema)
    Q17          = fields.Nested(ActualExpectedSelectionSchema)
    Q18          = fields.Nested(ActualExpectedSelectionSchema)
    Q19          = fields.Nested(ActualExpectedSelectionSchema)
    Q20          = fields.Nested(ActualExpectedSelectionSchema)
    Q21          = fields.Nested(ActualExpectedSelectionSchema)
    Q22          = fields.Nested(ActualExpectedSelectionSchema)
    Q23          = fields.Nested(ActualExpectedSelectionSchema)
    Q24          = fields.Nested(ActualExpectedSelectionSchema)
    Q25          = fields.Nested(ActualExpectedSelectionSchema)
    Q26          = fields.Nested(ActualExpectedSelectionSchema)
    Q27          = fields.Nested(ActualExpectedSelectionSchema)
    Q28          = fields.Nested(ActualExpectedSelectionSchema)
    Q29          = fields.Nested(ActualExpectedSelectionSchema)
    Q30          = fields.Nested(ActualExpectedSelectionSchema)
    Q31          = fields.Nested(ActualExpectedSelectionSchema)
    Q32          = fields.Nested(ActualExpectedSelectionSchema)
    Q33          = fields.Nested(ActualExpectedSelectionSchema)
    Q34          = fields.Nested(ActualExpectedSelectionSchema)
    Q35          = fields.Nested(ActualExpectedSelectionSchema)
    Q36          = fields.Nested(ActualExpectedSelectionSchema)
    Q37          = fields.Nested(ActualExpectedSelectionSchema)
    Q38          = fields.Nested(ActualExpectedSelectionSchema)
    Q39          = fields.Nested(ActualExpectedSelectionSchema)
    Q40          = fields.Nested(ActualExpectedSelectionSchema)
    Q41          = fields.Nested(ActualExpectedSelectionSchema)
    Q42          = fields.Nested(ActualExpectedSelectionSchema)
    Q43          = fields.Nested(ActualExpectedSelectionSchema)
    Q44          = fields.Nested(ActualExpectedSelectionSchema)
    Q45          = fields.Nested(ActualExpectedSelectionSchema)
    Q46          = fields.Nested(ActualExpectedSelectionSchema)
    Q47          = fields.Nested(ActualExpectedSelectionSchema)
    Q48          = fields.Nested(ActualExpectedSelectionSchema)
    Q49          = fields.Nested(ActualExpectedSelectionSchema)
    Q50          = fields.Nested(ActualExpectedSelectionSchema)

class ScantronSchema(Schema):
    scantron_id  = fields.Integer()
    scantron_url = fields.Str()
    name         = fields.Str()
    subject      = fields.Str()
    score        = fields.Integer()
    result       = fields.Nested(SubmissionResultsSchema)

class AnswerKeysSchema(Schema):
    Q1           = fields.Str(Required=True)
    Q2           = fields.Str(Required=True)
    Q3           = fields.Str(Required=True)
    Q4           = fields.Str(Required=True)
    Q5           = fields.Str(Required=True)
    Q6           = fields.Str(Required=True)
    Q7           = fields.Str(Required=True)
    Q8           = fields.Str(Required=True)
    Q9           = fields.Str(Required=True)
    Q10          = fields.Str(Required=True)
    Q11          = fields.Str(Required=True)
    Q12          = fields.Str(Required=True)
    Q13          = fields.Str(Required=True)
    Q14          = fields.Str(Required=True)
    Q15          = fields.Str(Required=True)
    Q16          = fields.Str(Required=True)
    Q17          = fields.Str(Required=True)
    Q18          = fields.Str(Required=True)
    Q19          = fields.Str(Required=True)
    Q20          = fields.Str(Required=True)
    Q21          = fields.Str(Required=True)
    Q22          = fields.Str(Required=True)
    Q23          = fields.Str(Required=True)
    Q24          = fields.Str(Required=True)
    Q25          = fields.Str(Required=True)
    Q26          = fields.Str(Required=True)
    Q27          = fields.Str(Required=True)
    Q28          = fields.Str(Required=True)
    Q29          = fields.Str(Required=True)
    Q30          = fields.Str(Required=True)
    Q31          = fields.Str(Required=True)
    Q32          = fields.Str(Required=True)
    Q33          = fields.Str(Required=True)
    Q34          = fields.Str(Required=True)
    Q35          = fields.Str(Required=True)
    Q36          = fields.Str(Required=True)
    Q37          = fields.Str(Required=True)
    Q38          = fields.Str(Required=True)
    Q39          = fields.Str(Required=True)
    Q40          = fields.Str(Required=True)
    Q41          = fields.Str(Required=True)
    Q42          = fields.Str(Required=True)
    Q43          = fields.Str(Required=True)
    Q44          = fields.Str(Required=True)
    Q45          = fields.Str(Required=True)
    Q46          = fields.Str(Required=True)
    Q47          = fields.Str(Required=True)
    Q48          = fields.Str(Required=True)
    Q49          = fields.Str(Required=True)
    Q50          = fields.Str(Required=True)

class NewTestSchema(Schema):
    test_id      = fields.Integer()
    subject      = fields.Str(Required=True)
    answer_keys  = fields.Nested(AnswerKeysSchema, Required=True)
    submissions  = fields.List(fields.Nested(ScantronSchema))

def createDbObjects():
    conn = sqlite3.connect('scantron.db')
    c = conn.cursor()

    # Create table
    c.execute('''CREATE TABLE if not exists tests
                 (id INTEGER PRIMARY KEY, 
                 subject TEXT)''')

    c.execute('''CREATE UNIQUE INDEX if not exists tests_subject_unq ON tests(subject)''')

    c.execute('''CREATE TABLE if not exists test_answer_keys
                 (test_id INTEGER, 
                 question_number TEXT, 
                 answer_key TEXT, 
                 PRIMARY KEY(test_id,question_number))''')

    c.execute('''CREATE TABLE if not exists submissions
                 (id INTEGER PRIMARY KEY, 
                 test_id INTEGER, 
                 answer_image BLOB)''')

    c.execute('''CREATE TABLE if not exists submission_answer_keys
                 (submission_id INTEGER, 
                 question_number TEXT, 
                 answer_key TEXT,
                 PRIMARY KEY(submission_id, question_number))''')
    conn.commit()

app = Flask(__name__)
createDbObjects()

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad Request'}), 400)

@app.route('/api/tests', methods=['POST'])
def new_test():
    if not request.json:
        abort(400)
    else:
        try:
            result = NewTestSchema().load(request.json)
        except ValidationError as err:
            return jsonify({'err_messages' : err.messages, 'err_valid_data' : err.valid_data})

    conn = sqlite3.connect('scantron.db')
    c = conn.cursor()
    insert_tests = '''INSERT INTO tests(subject) VALUES (?)'''
    insert_test_answers = '''INSERT INTO test_answer_keys(test_id,question_number,answer_key) VALUES (?,?,?)'''

    subject = (request.json['subject'],)
    c.execute(insert_tests,subject)
    test_id = c.lastrowid
    for question in request.json['answer_keys']:
        c.execute(insert_test_answers, (test_id, question, request.json['answer_keys'][question]))

    result['test_id'] = test_id
    result.update(request.json)
    conn.commit()
    return jsonify(result)




students = [
    {
        'id': 1,
        'name': u'John Doe',
        'classes': [1,2,3,4], 
    },
    {
        'id': 2,
        'name': u'Jane Doe',
        'classes': [2,4], 
    }
]
classes = [
    {
        'id':1,
        'name': 'CMPE-273',
        'students' : [1]
    },
    {
        'id':2,
        'name': 'CMPE-281',
        'students' : [1,2]
    },
    {
        'id':3,
        'name': 'CMPE-280',
        'students' : [1]
    },
    {
        'id':4,
        'name': 'CMPE-272',
        'students' : [1,2]
    },
]



@app.route('/hello')
def hello():
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'

@app.route('/students', methods=['GET'])
def get_students():
    c = []
    for s in students:
        c.append({'name' : s['name']})
    return jsonify({'students': c})

@app.route('/student_classes', methods=['GET'])
def get_student_classes():
    stu_list = copy.deepcopy(students)
    for s in stu_list:
        c = []
        for id in s['classes']:
            # print(id)
            for cl in classes:
                if id == cl['id']:
                    c.append(cl)
        s['classes'] = c
    return jsonify({'students': stu_list})

@app.route('/classes', methods=['GET'])
def get_classes():
    c = []
    for cl in classes:
        c.append({'name' : cl['name']})
    return jsonify({'classes': c})

@app.route('/class_students', methods=['GET'])
def get_class_students():
    class_list = copy.deepcopy(classes)
    for c in class_list:
        s = []
        for id in c['students']:
            for st in students:
                if id == st['id']:
                    s.append(st)
        c['students'] = s
    return jsonify({'students': class_list})

@app.route('/student/<int:student_id>', methods=['GET'])
def get_student_from_id(student_id):
    s = [s for s in students if s['id'] == student_id]
    if len(s) == 0:
        abort(404)
    return jsonify({'student': s[0]['name']})

@app.route('/class/<int:class_id>', methods=['GET'])
def get_class_from_id(class_id):
    s = [s for s in classes if s['id'] == class_id]
    if len(s) == 0:
        abort(404)
    return jsonify({'class': s[0]['name']})

@app.route('/classes', methods=['POST'])
def new_class():
    if not request.json or not 'name' in request.json:
        abort(400)
    s = {
        'id': classes[-1]['id'] + 1,
        'name' : request.json['name'],
        'students' : request.json['students']
    }
    classes.append(s)
    return jsonify({'class': s})

@app.route('/class/<int:class_id>', methods=['PATCH'])
def add_student_to_class(class_id):
    if not request.json or not 'student_id' in request.json:
        abort(400)
    
    s = [s for s in classes if s['id'] == class_id]
    if len(s) == 0:
        abort(404)

    s[0]['students'].append(request.json['student_id'])

    cl = copy.deepcopy(s[0])
    c = []
    for id in cl['students']:
        # print(id)
        for st in students:
            if id == st['id']:
                c.append(st)
    cl['students'] = c

    return jsonify(cl), 201
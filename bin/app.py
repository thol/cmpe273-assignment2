from flask import Flask, escape, request, jsonify, abort, make_response
import copy
import sqlite3

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

conn = sqlite3.connect('scantron.db')

c = conn.cursor()

# Create table
c.execute('''CREATE TABLE if not exists tests
             (id INTEGER PRIMARY KEY, subject text)''')

c.execute('''CREATE TABLE if not exists test_answer_keys
             (test_id INTEGER, question_number INTEGER, answer_key text)''')

c.execute('''CREATE TABLE if not exists submissions
             (id INTEGER PRIMARY KEY, test_id INTEGER, answer_image BLOB)''')

c.execute('''CREATE TABLE if not exists submission_answer_keys
             (submission_id INTEGER, question_number INTEGER, answer_key text)''')

conn.commit()

app = Flask(__name__)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

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

@app.route('/students', methods=['POST'])
def new_student():
    if not request.json or not 'name' in request.json:
        abort(400)
    s = {
        'id': students[-1]['id'] + 1,
        'name' : request.json['name'],
        'classes' : request.json['classes']
    }
    students.append(s)
    return jsonify({'student': s})

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
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

class NewAnswerSchema(Schema):
    scantron_id  = fields.Integer()
    name         = fields.Str(Required=True)
    subject      = fields.Str(Required=True)
    answers      = fields.Nested(AnswerKeysSchema, Required=True)


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
                 name TEXT,
                 answer_image BLOB,
                 score INTEGER)''')
    c.execute('''CREATE UNIQUE INDEX if not exists submission_name_unq ON submissions(name)''')

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
    return make_response(jsonify({'error': 'Bad Request1'}), 400)

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

def test_id_exists(test_id):
    conn = sqlite3.connect('scantron.db')
    c = conn.cursor()
    query_test_id = '''SELECT count(*) FROM tests where id = ?'''
    query_tuple = (test_id,)
    cursor = c.execute(query_test_id,query_tuple)
    for row in cursor:
        count = row[0]
    if count > 0:
        return True
    else:
        return False

def build_submission_result(submission_id):
    result = {}
    result['scantron_id'] = submission_id
    result['scantron_url'] = "http://localhost:5000/files/scantron-"+ str(submission_id) +".json"

    conn = sqlite3.connect('scantron.db')
    c = conn.cursor()
    query_result = '''
        select s.name, t.subject, s.score, tak.question_number, tak.answer_key, sak.answer_key
        from test_answer_keys tak, submission_answer_keys sak, submissions s, tests t
        where tak.question_number = sak.question_number
        and sak.submission_id = s.id
        and s.test_id = tak.test_id
        and s.id = ?
        and s.test_id = t.id
    '''
    query_tuple = (submission_id,)
    cursor = c.execute(query_result,query_tuple)
    for row in cursor:
        result['name'] = row[0]
        result['subject'] = row[1]
        result['score'] = row[2]
        q_no = row[3]
        result[q_no] = {}
        result[q_no]['actual'] = row[4]
        result[q_no]['expected'] = row[5]

    return result


def process_scantron_file(test_id, answer_json, answer_str):
    answer_blob = sqlite3.Binary(json.dumps(answer_str).encode('utf-8'))
    conn = sqlite3.connect('scantron.db')
    c = conn.cursor()
    insert_submission = '''INSERT INTO submissions (test_id, name, answer_image) VALUES (?,?, ?)'''
    submission_tuple = (test_id, answer_json['name'], answer_blob)
    c.execute(insert_submission, submission_tuple)
    submission_id = c.lastrowid

    insert_submission_answers = '''INSERT INTO submission_answer_keys(submission_id,question_number,answer_key) VALUES (?,?,?)'''
    for question in answer_json['answers']:
        c.execute(insert_submission_answers, (submission_id, question, answer_json['answers'][question]))

    get_score = '''
    select count(*)
    from test_answer_keys tak, submission_answer_keys sak, submissions s
    where tak.question_number = sak.question_number
    and tak.answer_key = sak.answer_key
    and sak.submission_id = s.id
    and s.test_id = tak.test_id
    and s.id = ?
    '''
    get_score_tuple = (submission_id,)
    cursor = c.execute(get_score, get_score_tuple)
    for row in cursor:
        count = row[0]

    update_score = '''UPDATE submissions SET score = ? WHERE id = ?'''
    update_score_tuple = (count, submission_id)
    c.execute(update_score, update_score_tuple)
    conn.commit()

    return build_submission_result(submission_id)


@app.route('/api/tests/<int:test_id>/scantrons', methods=['POST'])
def new_scantron(test_id):
    # print('request.method', request.method)
    # print('request.args', request.args)
    # print('request.form', request.form)
    # print('request.files', request.files)

    # 'file' not in .. abort doesn't work PAINFUL only IN works (may be due to reuse of 'result')
    if 'file' in request.files:
        answer_str = str(request.files['file'].read(),'utf-8')
        # print(answer_str)
        answer_json = json.loads(answer_str)
        try:
            answer_obj = NewAnswerSchema().load(answer_json)
        except ValidationError as err:
            return jsonify({'err_messages' : err.messages, 'err_valid_data' : err.valid_data})
    else:
        abort(404)

    if (test_id_exists(test_id)):
        submission_result = process_scantron_file(test_id, answer_json, answer_str)
    else:
        abort(404)

    return jsonify(submission_result)


def build_test_answer_result(test_id):
    result = {}

    conn = sqlite3.connect('scantron.db')
    c = conn.cursor()
    query_result = '''
        select tak.question_number, tak.answer_key
        from test_answer_keys tak
        where tak.test_id = ?
    '''
    query_tuple = (test_id,)
    cursor = c.execute(query_result,query_tuple)
    for row in cursor:
        q_no = row[0]
        result[q_no] = row[1]

    return result

def build_submission_data(test_id):
    result = {}
    result['submissions'] = [] 
    conn = sqlite3.connect('scantron.db')
    c = conn.cursor()
    query_submission_meta = '''SELECT id FROM submissions where test_id = ?'''
    query_tuple = (test_id,)
    cursor = c.execute(query_submission_meta,query_tuple)
    for row in cursor:
        submission_id = row[0]
        result['submissions'].append(build_submission_result(submission_id))
    return result

def get_test_submission_data(test_id):
    test_data = {}
    conn = sqlite3.connect('scantron.db')
    c = conn.cursor()
    query_test_meta = '''SELECT subject FROM tests where id = ?'''
    query_tuple = (test_id,)
    cursor = c.execute(query_test_meta,query_tuple)
    for row in cursor:
        subject = row[0]

    test_data['test_id'] = test_id
    test_data['subject'] = subject
    test_data['answer_keys'] = build_test_answer_result(test_id)

    submission_result = build_submission_data(test_id)
    test_data.update(submission_result)

    return test_data

@app.route('/api/tests/<int:test_id>', methods=['GET'])
def get_submissions(test_id):

    if (test_id_exists(test_id)):
        test_submission_data = get_test_submission_data(test_id)
    else:
        abort(404)

    return jsonify(test_submission_data)

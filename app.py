#!flask/bin/python
from flask import Flask, jsonify, request
from model import connect_to_db, Tasks, db

app = Flask(__name__)

@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    tasks = [t.to_dict() for t in Tasks.query.all()]
    return jsonify(tasks=tasks)

if __name__ == '__main__':
    connect_to_db(app)
    app.run(debug=True)
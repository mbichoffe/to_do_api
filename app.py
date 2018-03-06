#!flask/bin/python
from flask import Flask, jsonify, request, make_response
from model import connect_to_db, Tasks, db

app = Flask(__name__)

@app.route('/todo/api/v1.0/tasks', methods=['GET', 'POST'])
def get_tasks():
    tasks = [t.to_dict() for t in Tasks.query.all()]
    return jsonify(tasks=tasks)

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    t = Tasks.query.get_or_404(task_id)
    return jsonify(t.to_dict())


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    connect_to_db(app)
    app.run(debug=True)
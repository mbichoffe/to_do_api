#!flask/bin/python
from flask import Flask, jsonify, request, make_response, abort
from model import connect_to_db, Tasks, db

app = Flask(__name__)

@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():

    tasks = [t.to_dict() for t in Tasks.query.all()]
    return jsonify(tasks=tasks)

@app.route('/todo/api/v1.0/tasks', methods=['POST'])
def add_tasks():
    if not request.json or 'title' not in request.json:
        abort(400)
    else:
        new_task = Tasks(task_title=request.json['title'],
                         task_description=request.json.get('description', ''))
        db.session.add(new_task)
        db.session.commit()

    # Return HTTP status code 201 (the code for created), with body being new ID
    return jsonify(new_task.task_id), 201


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
#!flask/bin/python
from flask import Flask, jsonify, request, make_response, abort, url_for
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


@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['PUT', 'PATCH'])
def update_task(task_id):
    t = Tasks.query.get_or_404(task_id)
    if not request.json:
        abort(400)
    if 'title' in request.json:
        if type(request.json['title']) != unicode:
            abort(400)
        t.task_title = request.json['title']

    if 'description' in request.json:
        if type(request.json['description']) != unicode:
            abort(400)
        t.task_description = request.json['description']

    if 'done' in request.json:
        if type(request.json['done']) is not bool:
            abort(400)

    db.session.commit()

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


### HELPER FUNCTION ###
# def make_public_task(task):


if __name__ == '__main__':
    connect_to_db(app)
    app.run(debug=True)
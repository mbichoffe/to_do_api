#!flask/bin/python
"""Flask server that demonstrates serving APIs.

Serves similar same API twice, both by hand and using Flask-restless.

/api : created using Flask-restless
  /api/tasks

/api2 : created by making routes and doing work directly
  /api2/v1.0/tasks

"""
from flask import Flask, jsonify, request, make_response, abort, url_for
from flask_httpauth import HTTPBasicAuth
from model import connect_to_db, Tasks, db

app = Flask(__name__)
auth = HTTPBasicAuth()


@app.route('/todo/api2/v1.0/tasks', methods=['GET'])
def get_tasks():

    tasks = [to_dict(t) for t in Tasks.query.all()]
    return jsonify(tasks=tasks)


@app.route('/todo/api2/v1.0/tasks', methods=['POST'])
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


@app.route('/todo/api2/v1.0/tasks/<int:task_id>', methods=['GET'])
@auth.login_required
def get_task(task_id):
    t = Tasks.query.get_or_404(task_id)
    return jsonify(to_dict(t))


@app.route('/todo/api2/v1.0/tasks/<int:task_id>', methods=['PUT', 'PATCH'])
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
        t.task_completed = request.json['done']

    db.session.commit()
    # Return status code 200, with body being ID updated
    return jsonify(to_dict(t)), 200


@app.route('/todo/api2/v1.0/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Remove task from db."""
    t = Tasks.query.get_or_404(task_id)
    t.delete()
    db.session.commit()

    return jsonify(""), 200


@app.errorhandler(404)
def not_found(error):
    """Return json for 404 error"""
    return make_response(jsonify({'error': 'Not found'}), 404)


@auth.get_password
def get_password(username):
    #TO DO: implement users and api keys on our db
    if username == 'marina':
        return 'python'
    return None


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)

### HELPER FUNCTION ###

def to_dict(task):
    """Turn an employee object into a dictionary."""
    return {
        'id': task.task_id,
        'title': task.task_title,
        'description': task.task_description,
        'completed': task.task_completed,
        'uri': url_for('get_task', task_id=task.task_id, _external=True)
    }


if __name__ == '__main__':
    connect_to_db(app)
    app.run(debug=True)
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Models and database functions for Purchase Analysis project."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

##############################################################################
# Model definitions

class Tasks(db.Model):

    __tablename__ = "tasks"

    task_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    task_title = db.Column(db.String, index=True)
    task_description = db.Column(db.String(100))
    task_completed = db.Column(db.Boolean, default=False)
    task_uri = db.Column(db.String, nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""
        return "<Task id={} title={} description={} completed={}".format(
            self.task_id,
            self.task_title,
            self.task_description,
            self.task_completed)

    def to_dict(self):
        """Turn an employee object into a dictionary."""
        return {
            'id': self.task_id,
            'title': self.task_title,
            'description': self.task_description,
            'completed': self.task_completed,
            'uri': self.task_uri or None
        }


def example_data():
    """Create some sample data."""
    # In case this is run more than once, empty existing data
    Tasks.query.delete()

    # Reset PostgreSQL sequence:
    # Now we'll start adding employees with ID #1
    db.session.execute(
        "SELECT setval('tasks_task_id_seq', 1, false)")

    # Add sample employees and departments
    task1 = Tasks(task_title=u'Learn Python',
                  task_description=u'Need to find a good Python tutorial on the web',
                  task_uri=None)

    task2 = Tasks(task_title=u'Buy groceries',
                  task_description=u'Milk, Cheese, Pizza, Fruit, Tylenol',
                  task_uri=None)

    db.session.add_all(
        [task1, task2])
    db.session.commit()


def connect_to_db(app, db_uri="postgresql:///tasks"):
    """Connect the database to our Flask app."""
    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_ECHO'] = False
    db.app = app
    db.init_app(app)

    # Create table and fill DB with example data
    db.create_all()
    example_data()

if __name__ == "__main__":
    # As a convenience, if you run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from app import app

    connect_to_db(app)
    print("Connected to DB.")

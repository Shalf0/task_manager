"""
CRUD TASKs
Get view filters by status, ending_date
View update ending_date
View update status

"""
from flask import Blueprint, request, jsonify, url_for, g
from datetime import datetime

from .models import Task, db
from task_manager.auth.views import auth


task_module = Blueprint('tasks', __name__)


@task_module.route('/api/tasks', methods=['POST'])
@auth.login_required
def create_task():
    name = request.json.get('name')
    if request.json.get('description') is not None:
        description = request.json.get('description')
    else:
        description = None
    status = 0  # По умолчанию status = 0
    ending_date = request.json.get('ending_date')
    created_at = datetime.now()
    user_id = g.user.id

    task = Task(name=name, description=description, status=status,
                ending_date=ending_date, created_at=created_at,
                user_id=user_id)
    db.session.add(task)
    db.session.commit()

    return jsonify(
        ({'Task name': task.name}), 201,
        {'URI': url_for('tasks.create_task', id=task.id, _external=True)})


@task_module.route('/api/tasks', methods=['GET'])
@auth.login_required
def get_tasks():
    query = Task.query.filter_by(user_id=g.user.id).all()
    all_tasks = [{'id': task.id,
                  'name': task.name,
                  'description': task.description,
                  'status': task.status,
                  'ending_date': task.ending_date,
                  'created_at': task.created_at} for task in query]
    return jsonify(all_tasks)

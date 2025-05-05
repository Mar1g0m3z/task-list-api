from flask import Blueprint, abort, make_response, request, Response
from app.models.task import Task
from ..db import db
from .route_utilities import validate_model

task_bp = Blueprint("task_bp", __name__, url_prefix="/tasks")


@task_bp.post("")
def create_task():
    request_body = request.get_json()
    new_task = Task.from_dict(request_body)

    db.session.add(new_task)
    db.session.commit()
    return {"task": new_task.to_dict()}, 201


@task_bp.get("")
def get_all_tasks():
    query = db.select(Task)
    title_param = request.args.get("title")
    if title_param:
        query = query.where(Task.name == title_param)

    tasks = db.session.scalars(query)
    tasks_response = [task.to_dict() for task in tasks]
    return tasks_response


@task_bp.get("/<id>")
def get_one_task(id):
    task = validate_model(Task, id)
    return {"task": task.to_dict()}

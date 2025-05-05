from flask import Blueprint, abort, make_response, request, Response
from app.models.task import Task
from ..db import db
from .route_utilities import validate_model

task_bp = Blueprint("task_bp", __name__, url_prefix="/tasks")


@task_bp.get("")
def get_all_tasks():
    query = db.select(Task)
    title_param = request.args.get("title")
    if title_param:
        query = query.where(Task.name == title_param)

    tasks = db.session.scalars(query)
    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_dict())
    return tasks_response


@task_bp.get("/<id>")
def get_one_task(id):
    task = validate_model(Task, id)
    return task.to_dict()

from flask import Blueprint, abort, make_response, request, Response
from app.models.task import Task
from ..db import db
from .route_utilities import validate_model, send_slack_message
from datetime import datetime, timezone

task_bp = Blueprint("task_bp", __name__, url_prefix="/tasks")


@task_bp.delete("/<id>")
def delete_task(id):
    task = validate_model(Task, id)
    db.session.delete(task)
    db.session.commit()
    return Response(status=204, mimetype="application/json")


@task_bp.put("/<id>")
def update_task(id):
    task = validate_model(Task, id)
    request_body = request.get_json()
    task.title = request_body["title"]
    task.description = request_body["description"]
    db.session.commit()
    return Response(status=204, mimetype="application/json")


@task_bp.post("")
def create_task():
    request_body = request.get_json()

    if not request_body.get("title") or not request_body.get("description"):
        return {"details": "Invalid data"}, 400

    new_task = Task.from_dict(request_body)

    db.session.add(new_task)
    db.session.commit()
    return {"task": new_task.to_dict()}, 201


@task_bp.get("")
def get_all_tasks():
    sort_param = request.args.get("sort")
    query = db.select(Task)

    if sort_param == "asc":
        query = query.order_by(Task.title.asc())
    elif sort_param == "desc":
        query = query.order_by(Task.title.desc())
    title_param = request.args.get("title")

    if title_param:
        query = query.where(Task.name == title_param)

    tasks = db.session.scalars(query)
    tasks_response = [task.to_dict() for task in tasks]
    return tasks_response


@task_bp.get("/<id>")
def get_one_task(id):
    task = validate_model(Task, id)
    return {"task": task.to_dict(include_goal_id=True)}


@task_bp.patch("/<id>/mark_complete")
def mark_task_complete(id):
    task = validate_model(Task, id)

    task.completed_at = datetime.now(timezone.utc)
    db.session.commit()

    send_slack_message(task.title)
    return Response(status=204, mimetype="application/json")


@task_bp.patch("/<id>/mark_incomplete")
def mark_task_incomplete(id):
    task = validate_model(Task, id)
    task.completed_at = None
    db.session.commit()
    return Response(status=204, mimetype="application/json")

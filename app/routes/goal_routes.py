from flask import Blueprint, abort, make_response, request, Response
from app.models.goal import Goal
from ..db import db
from .route_utilities import validate_model

goal_bp = Blueprint("goal_bp", __name__, url_prefix="/goals")


@goal_bp.get("")
def get_all_goals():
    query = db.select(Goal)
    goals = db.session.scalars(query)
    goal_response = [goal.to_dict() for goal in goals]

    return goal_response


@goal_bp.get("/<id>")
def get_one_goal(id):
    goal = validate_model(Goal, id)
    return {"goal": goal.to_dict()}


@goal_bp.post("")
def create_goal():
    request_body = request.get_json()

    if not request_body.get("title"):
        return {"details": "Invalid data"}, 400

    new_goal = Goal.from_dict(request_body)

    db.session.add(new_goal)
    db.session.commit()

    return {"goal": new_goal.to_dict()}, 201


@goal_bp.put("/<id>")
def update_goal(id):
    goal = validate_model(Goal, id)
    request_body = request.get_json()
    goal.title = request_body["title"]

    db.session.commit()
    return Response(status=204, mimetype="application/json")


@goal_bp.delete("/<id>")
def delete_goal(id):
    goal = validate_model(Goal, id)
    db.session.delete(goal)
    db.session.commit()
    return Response(status=204, mimetype="application/json")

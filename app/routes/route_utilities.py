from flask import abort, make_response, jsonify
import requests
from ..db import db
import os


SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
SLACK_CHANNEL = os.environ.get("SLACK_CHANNEL")


def validate_model(cls, modelid):
    try:
        model_id = int(modelid)
    except ValueError:
        invalid_response = {
            "message": f"{cls.__name__} id ({model_id}) is invalid."}
        abort(make_response(invalid_response, 400))

    query = db.select(cls).where(cls.id == model_id)
    model = db.session.scalar(query)

    if not model:
        not_found = {
            "message": f"{cls.__name__} with id ({model_id}) not found."}
        abort(make_response(not_found, 404))
    return model


def send_slack_message(task_title):
    url = "https://slack.com/api/chat.postMessage"

    headers = {
        "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
        "Content-Type": "application/json; charset=UTF-8"
    }
    payload = {
        "channel": SLACK_CHANNEL,
        "text": f"Someone just completed the task {task_title}"

    }
    response = requests.post(url, headers=headers, json=payload)

    if not response.ok or not response.json().get("ok"):
        print("Failed to send slack message:", response.text)

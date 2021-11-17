from flask import Flask, request, jsonify
from celery.result import AsyncResult
from tasks import celery_app, calc_tags, calc_tags_long


app = Flask(__name__)


@app.route("/tags", methods=["POST"])
def tags():
    request_data = request.get_json()
    if not request_data:
        return "WHERE IS MY JSON, MATE?"

    url = None
    if "website" in request_data:
        url = request_data["website"]
    if not url:
        return "GOT NO URL"

    task = calc_tags.delay(url)

    response = {
        "task_id": task.id,
    }
    return jsonify(response)


@app.route("/tags/<task_id>", methods=["GET"])
def tags_get(task_id):
    task = AsyncResult(task_id, app=celery_app)

    if task.state == "PENDING":
        response = {
            "state": task.state,
            "ready": task.ready(),
        }
        return jsonify(response)

    result = task.get(timeout=10)
    response = {
        "the_data": result,
    }
    return jsonify(response)


@app.route("/tags_long", methods=["POST"])
def tags_long():
    """create long running task"""
    request_data = request.get_json()
    if not request_data:
        return "WHERE IS MY JSON, MATE?"

    url = None
    if "website" in request_data:
        url = request_data["website"]
    if not url:
        return "GOT NO URL"

    task = calc_tags_long.delay(url)

    response = {
        "task_id": task.id,
    }
    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)

from fastapi import FastAPI, Request
from json.decoder import JSONDecodeError
from celery.result import AsyncResult
from tasks import celery_app, calc_tags, calc_tags_long

app = FastAPI()


@app.post("/tags")
async def tags(request: Request):
    try:
        request_data = await request.json()
    except JSONDecodeError:
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
    return response


@app.get("/tags/{task_id}")
async def tags_get(task_id):
    task = AsyncResult(task_id, app=celery_app)

    if task.state == "PENDING":
        response = {
            "state": task.state,
            "ready": task.ready(),
        }
        return response

    result = task.get(timeout=10)
    response = {
        "the_data": result,
    }
    return response


@app.post("/tags_long")
async def tags_long(request: Request):
    """create long running task"""
    try:
        request_data = await request.json()
    except JSONDecodeError:
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
    return response

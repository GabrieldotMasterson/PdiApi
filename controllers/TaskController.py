from datetime import datetime

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, current_user
from sqlalchemy import select
from spectree import Response

from utils.Factory import api, db
from models.PDI.TaskModel import TaskModel, TaskResponseList, TaskCreate
from utils.responses import DefaultResponse

task_controller = Blueprint("task_controller", __name__, url_prefix="/tasks")

@task_controller.get("/")
@api.validate(resp=Response(HTTP_200=DefaultResponse), tags=["tasks"])
@jwt_required()
def get_tasks():
    """
    Retorna a lista de Tasks
    """
    tasks = db.session.scalars(select(TaskModel)).all()

    response = {
        "tasks": [task.title for task in tasks]
    }

    return response, 200

@task_controller.post("/")
@api.validate(
    json=TaskCreate,
    resp=Response(HTTP_201=DefaultResponse, HTTP_400=DefaultResponse),
    tags=["tasks"]
)
@jwt_required()
def create_task():
    data = request.json

    task = TaskModel(
        title=data["title"],
        description=data["description"],
        user_id=current_user.id
    )

    db.session.add(task)
    db.session.commit()

    return {"msg": "Task criado com sucesso"}, 201

@task_controller.get("/<int:task_id>")
@api.validate(
    resp=Response(HTTP_200=TaskResponseList, HTTP_404=DefaultResponse), tags=["tasks"]
)
@jwt_required()
def get_task(task_id):
    task = db.session.get(TaskModel, task_id)
    if task is None:
        return {"msg": f"Task não encontrado {task_id}"}, 404

    response = TaskResponseList(
        task=task.title
    ).model_dump()

    return response, 200


@task_controller.delete("/<int:task_id>")
@api.validate(
    resp=Response(HTTP_200=DefaultResponse, HTTP_404=DefaultResponse), tags=["tasks"]
)
@jwt_required()
def delete_task(task_id):
    task = db.session.get(TaskModel, task_id)
    if task is None:
        return {"msg": f"Task não encontrado {task_id}"}, 404

    db.session.delete(task)
    db.session.commit()

    return {"msg": "Task deletado com sucesso"}, 200

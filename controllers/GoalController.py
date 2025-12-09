from datetime import datetime

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, current_user
from sqlalchemy import select
from spectree import Response

from utils.Factory import api, db
from models.PDI.GoalModel import GoalModel, GoalResponseList, GoalCreate
from utils.responses import DefaultResponse

goal_controller = Blueprint("goal_controller", __name__, url_prefix="/goals")

@goal_controller.get("/")
@api.validate(resp=Response(HTTP_200=DefaultResponse), tags=["goals"])
@jwt_required()
def get_goals():
    """
    Retorna a lista de metas
    """
    goals = db.session.scalars(select(GoalModel)).all()

    response = {
        "goals": [goal.title for goal in goals]
    }

    return response, 200

@goal_controller.post("/")
@api.validate(
    json=GoalCreate,
    resp=Response(HTTP_201=DefaultResponse, HTTP_400=DefaultResponse),
    tags=["goals"]
)
@jwt_required()
def create_goal():
    data = request.json

    goal = GoalModel(
        title=data["title"],
        description=data["description"],
        user_id=current_user.id
    )

    db.session.add(goal)
    db.session.commit()

    return {"msg": "meta criada com sucesso"}, 201

@goal_controller.get("/<int:goal_id>")
@api.validate(
    resp=Response(HTTP_200=GoalResponseList, HTTP_404=DefaultResponse), tags=["goals"]
)
@jwt_required()
def get_goal(goal_id):
    goal = db.session.get(GoalModel, goal_id)
    if goal is None:
        return {"msg": f"Goal não encontrado {goal_id}"}, 404

    response = GoalResponseList(
        title=goal.title,
        description=goal.description,
        user_id=goal.user_id
    ).model_dump()

    return response, 200

@goal_controller.delete("/<int:goal_id>")
@api.validate(
    resp=Response(HTTP_200=DefaultResponse, HTTP_404=DefaultResponse), tags=["goals"]
)
@jwt_required()
def delete_goal(goal_id):
    goal = db.session.get(GoalModel, goal_id)
    if goal is None:
        return {"msg": f"meta não encontrado {goal_id}"}, 404

    db.session.delete(goal)
    db.session.commit()

    return {"msg": "meta deletada com sucesso"}, 200

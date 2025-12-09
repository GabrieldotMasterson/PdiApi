from datetime import datetime

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, current_user
from sqlalchemy import select
from spectree import Response

from utils.Factory import api, db
from models.PDI.ProjectModel import ProjectModel, ProjectResponseList, ProjectCreate

from utils.responses import DefaultResponse

project_controller = Blueprint("project_controller", __name__, url_prefix="/projects")

@project_controller.get("/")
@api.validate(resp=Response(HTTP_200=DefaultResponse), tags=["projects"])
@jwt_required()
def get_projects():
    """
    Retorna a lista de Projects
    """
    projects = db.session.scalars(select(ProjectModel)).all()

    response = {
        "projects": [project.title for project in projects]
    }

    return response, 200

@project_controller.post("/")
@api.validate(
    json=ProjectCreate,
    resp=Response(HTTP_201=DefaultResponse, HTTP_400=DefaultResponse),
    tags=["projects"]
)
@jwt_required()
def create_project():
    data = request.json

    project = ProjectModel(
        title=data["title"],
        description=data["description"],
        user_id=current_user.id
    )

    db.session.add(project)
    db.session.commit()

    return {"msg": "Project criado com sucesso"}, 201

@project_controller.get("/<int:project_id>")
@api.validate(
    resp=Response(HTTP_200=ProjectResponseList, HTTP_404=DefaultResponse), tags=["projects"]
)
@jwt_required()
def get_project(project_id):
    project = db.session.get(ProjectModel, project_id)
    if project is None:
        return {"msg": f"Project não encontrado {project_id}"}, 404

    response = ProjectResponseList(
        project_id=project.id,
        title=project.title,
        description=project.description,
        created_at=project.created_at,
        user_id=project.user_id
    ).model_dump()

    return response, 200

@project_controller.delete("/<int:project_id>")
@api.validate(
    resp=Response(HTTP_200=DefaultResponse, HTTP_404=DefaultResponse), tags=["projects"]
)  
@jwt_required()
def delete_project(project_id):
    project = db.session.get(ProjectModel, project_id)
    if project is None:
        return {"msg": f"Project não encontrado {project_id}"}, 404

    db.session.delete(project)
    db.session.commit()

    return {"msg": "Project deletado com sucesso"}, 200

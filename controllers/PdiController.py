from datetime import datetime

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, current_user
from sqlalchemy import select
from spectree import Response

from utils.Factory import api, db
from models.PDI.PdiModel import PdiModel, PdiResponseList, PdiCreate
from utils.responses import DefaultResponse, ErrorResponse

pdi_controller = Blueprint("pdi_controller", __name__, url_prefix="/pdis")

@pdi_controller.get("/")
@api.validate(resp=Response(HTTP_200=DefaultResponse), tags=["pdis"])
@jwt_required()
def get_pdis():
    """
    Retporna a lista de PDIs
    """
    pdis = db.session.scalars(select(PdiModel)).all()

    response = {
        "pdis": [pdi.title for pdi in pdis]
    }

    return response, 200

@pdi_controller.post("/")
@api.validate(
    json=PdiCreate,
    resp=Response(HTTP_201=DefaultResponse, HTTP_400=ErrorResponse),
    tags=["pdis"]
)
@jwt_required()
def create_pdi():
    from ia.prompts import gerar_pdi_com_ia
    from models import GoalModel, ProjectModel, TaskModel

    data = request.json

    pdi = PdiModel(
        title=data["title"],
        description=data["description"],
        user_id=current_user.id
    )

    db.session.add(pdi)
    db.session.commit()

    ia_data = gerar_pdi_com_ia(data["title"], data["description"])

    # -------------------------------------
    # CRIAR METAS E SUAS TAREFAS
    # -------------------------------------
    for meta in ia_data["metas"]:
        goal = GoalModel(
            title=meta["titulo"],
            description=meta["descricao"],
            user_id=current_user.id,
            pdi_id=pdi.id
        )
        db.session.add(goal)
        db.session.commit()

        # criar tarefas da meta
        for tarefa in meta["tarefas"]:
            task = TaskModel(
                title=tarefa["titulo"],
                description=tarefa["descricao"],
                user_id=current_user.id,
                goal_id=goal.id
            )
            db.session.add(task)

    # -------------------------------------
    # CRIAR PROJETOS E SUAS TAREFAS
    # -------------------------------------
    for proj in ia_data["projetos"]:
        project = ProjectModel(
            title=proj["titulo"],
            description=proj["descricao"],
            user_id=current_user.id,
            pdi_id=pdi.id
        )
        db.session.add(project)
        db.session.commit()

        # tarefas do projeto
        for tarefa in proj["tarefas"]:
            task = TaskModel(
                title=tarefa["titulo"],
                description=tarefa["descricao"],
                user_id=current_user.id,
                project_id=project.id
            )
            db.session.add(task)

    db.session.commit()

    return {"msg": "PDI e recomendações geradas com sucesso!"}, 201


@pdi_controller.get("/<int:pdi_id>")
@api.validate(
    resp=Response(HTTP_200=PdiResponseList, HTTP_404=DefaultResponse), tags=["pdis"]
)
@jwt_required()
def get_pdi(pdi_id):
    pdi = db.session.get(PdiModel, pdi_id)
    if pdi is None:
        return {"msg": f"PDI não encontrado {pdi_id}"}, 404

    response = PdiResponseList(
        pdis=[pdi.title]
    ).model_dump()

    return response, 200

@pdi_controller.delete("/<int:pdi_id>")
@api.validate(
    resp=Response(HTTP_200=DefaultResponse, HTTP_404=DefaultResponse), tags=["pdis"]
)  
@jwt_required()
def delete_pdi(pdi_id):
    pdi = db.session.get(PdiModel, pdi_id)
    if pdi is None:
        return {"msg": f"PDI não encontrado {pdi_id}"}, 404

    db.session.delete(pdi)
    db.session.commit()

    return {"msg": "PDI deletado com sucesso"}, 200
# tabela de projetos de um Plano de Desenvolvimento Individual
from utils.Factory import db
from utils.models import OrmBase    
from models.PDI.TaskModel import TaskResponseSimple
from typing import List, Optional
from datetime import datetime, timezone
from pydantic import BaseModel

class ProjectModel(db.Model):
    __tablename__ = "project"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    pdi_id = db.Column(db.Integer, db.ForeignKey("pdi.id"), nullable=False)
    pdi = db.relationship("PdiModel", backref=db.backref("projects", lazy=True))
    is_completed = db.Column(db.Boolean, default=False)

    def __repr__(self) -> str:
        return f"<Project {self.name}>"
    
class ProjectResponse(OrmBase):
    id: int
    name: str
    description: str | None
    created_at: datetime
    pdi_id: int
    is_completed: bool

class ProjectCreate(BaseModel):
    name: str
    description: Optional[str]
    pdi_id: int

class ProjectResponseList(OrmBase):
    projects: List[ProjectResponse]

class ProjectDetailResponse(OrmBase):
    id: int
    name: str
    description: str | None
    created_at: datetime
    pdi_id: int
    is_completed: bool
    tasks: List[TaskResponseSimple]
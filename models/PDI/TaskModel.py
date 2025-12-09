#tabela das tarefas
# podem ser tanto das metas quanto dos projetos

from utils.Factory import db
from utils.models import OrmBase
from typing import List, Optional
from datetime import datetime, timezone
from pydantic import BaseModel

class TaskModel(db.Model):
    __tablename__ = "task"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    due_date = db.Column(db.DateTime, nullable=True)
    is_completed = db.Column(db.Boolean, default=False)

    # Foreign keys to either Goal or Project
    goal_id = db.Column(db.Integer, db.ForeignKey("goal.id"), nullable=True)
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"), nullable=True)

    def __repr__(self) -> str:
        return f"<Task {self.title}>"
    
class TaskResponse(OrmBase):
    id: int
    title: str
    description: str | None
    created_at: datetime
    due_date: datetime | None
    is_completed: bool
    goal_id: int | None
    project_id: int | None

class TaskResponseSimple(OrmBase):
    id: int
    title: str
    is_completed: bool

class TaskCreate(BaseModel):
    title: str
    description: Optional[str]
    due_date: Optional[datetime]
    goal_id: Optional[int]
    project_id: Optional[int]

class TaskResponseList(OrmBase):
    tasks: List[TaskResponse]

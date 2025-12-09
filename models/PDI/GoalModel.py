from datetime import datetime, timezone
from utils.Factory import db
from utils.models import OrmBase
from typing import List, Optional
from models.PDI.PdiModel import PdiModel
from pydantic import BaseModel

class GoalModel(db.Model):
    __tablename__ = "goal"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    pdi_id = db.Column(db.Integer, db.ForeignKey("pdi.id"), nullable=False)
    pdi = db.relationship("PdiModel", backref=db.backref("goals", lazy=True))
    is_completed = db.Column(db.Boolean, default=False)

    def __repr__(self) -> str:
        return f"<Goal {self.title}>"
    
class GoalResponse(OrmBase):
    id: int
    title: str
    description: str | None
    created_at: datetime
    pdi_id: int
    is_completed: bool

class GoalCreate(BaseModel):
    title: str
    description: Optional[str]
    pdi_id: int

class GoalResponseList(OrmBase):
    goals: List[GoalResponse]

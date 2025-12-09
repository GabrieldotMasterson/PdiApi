from datetime import datetime, timezone
from pydantic import BaseModel

from utils.Factory import db
from utils.models import OrmBase
from models.UserModel import UserResponseSimple
from typing import List, Optional

class PdiModel(db.Model):
    __tablename__ = "pdi"
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    owner = db.relationship("User", backref=db.backref("pdis", lazy=True))
    expected_deadline = db.Column(db.DateTime, nullable=True)
    deadline = db.Column(db.DateTime, nullable=True)
    last_updated = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    is_completed = db.Column(db.Boolean, default=False)

    progress = db.Column(db.Integer, default=0)  # 0-100

    is_specific = db.Column(db.Boolean, default=False)
    is_measurable = db.Column(db.Boolean, default=False)
    is_achievable = db.Column(db.Boolean, default=False)
    is_relevant = db.Column(db.Boolean, default=False)
    is_time_bound = db.Column(db.Boolean, default=False)

    category = db.Column(db.String(128))

    # student_id = db.Column(
    #     db.Integer,
    #     db.ForeignKey("student.id", ondelete="CASCADE"),
    #     nullable=False
    # )

    def __repr__(self) -> str:
        return f"<Pdi {self.title}>"
    
class PdiResponse(OrmBase):
    id: int
    title: str
    description: str | None
    created_at: datetime
    owner: UserResponseSimple
    expected_deadline: datetime | None
    deadline: datetime | None
    last_updated: datetime
    is_completed: bool
    progress: int
    is_specific: bool
    is_measurable: bool
    is_achievable: bool
    is_relevant: bool
    is_time_bound: bool
    category: str | None
    student_id: int

class PdiResponseList(BaseModel):
    pdis: List[PdiResponse]

class PdiCreate(BaseModel):
    title: str
    description: str | None
    created_at: datetime
    owner: UserResponseSimple
    expected_deadline: datetime | None
    deadline: datetime | None
    last_updated: datetime
    is_completed: bool
    progress: int
    is_specific: bool
    is_measurable: bool
    is_achievable: bool
    is_relevant: bool
    is_time_bound: bool
    category: str | None
    student_id: int

from sqlalchemy.orm import Mapped, mapped_column, relationship
# from sqlalchemy import ForeignKe
from typing import List
from ..db import db


class Goal(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(nullable=False)
    tasks: Mapped[List["Task"]] = relationship("Task", back_populates="goal")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            # "tasks": [task.to_dict() for task in self.tasks]
        }

    @classmethod
    def from_dict(cls, goal_data):
        return cls(title=goal_data["title"])

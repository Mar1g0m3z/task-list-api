from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import Optional
from sqlalchemy import ForeignKey
# from sqlalchemy import Datetime
from ..db import db


class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(nullable=False)
    goal_id: Mapped[Optional[int]] = mapped_column(ForeignKey("goal.id"))
    goal: Mapped[Optional["Goal"]] = relationship(
        "Goal", back_populates="tasks")
    description: Mapped[str] = mapped_column(nullable=False)
    completed_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)

    def to_dict(self, include_completed_at=False, include_goal_id=False):
        task_dict = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "is_complete": self.completed_at is not None,
            # "goal_id": self.goal.id if self.goal else None,  # Default to None
            # "goal_title": self.goal.title if self.goal else None  # Default to None

        }
        if include_goal_id and self.goal_id:
            task_dict["goal_id"] = self.goal_id
        return task_dict

    # if include_completed_at:
    #     task_dict["completed_at"] = self.completed_at

    # if include_goal_id and self.goal:
    #     task_dict["goal_id"] = self.goal.id
    #     task_dict["goal_title"] = self.goal.title
    # return task_dict

    @classmethod
    def from_dict(cls, task_data):
        return cls(
            title=task_data["title"],
            description=task_data["description"],
            completed_at=task_data.get("completed_at")
        )

from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
# from sqlalchemy import Datetime
from ..db import db


class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    completed_at: Mapped[datetime | None] = mapped_column(nullable=True)

    def to_dict(self, include_completed_at=False):
        task_dict = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "is_complete": bool(self.completed_at),
        }
        if include_completed_at:
            task_dict["completed_at"] = self.completed_at
        return task_dict

    # @classmethod
    def from_dict(cls, task_data):
        return cls(
            title=task_data["title"],
            description=task_data["description"],
            completed_at=task_data.get("completed_at"),
        )

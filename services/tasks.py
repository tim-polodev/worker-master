import datetime

from pymongo.database import Database

from models.tasks import TaskCreate


class TasksService:
    def __init__(self, db: Database):
        self.collection = db["tasks"]

    def add_task(self, task: TaskCreate):
        new_task = task.model_dump()
        new_task["created_at"] = datetime.datetime.now(datetime.UTC)
        new_task["updated_at"] = new_task["created_at"]
        new_task["status"] = "pending"  # Default status for new tasks
        insert_result = self.collection.insert_one(new_task)
        return self.collection.find_one({"_id": insert_result.inserted_id})

    def get_task_by_id(self, task_id):
        return self.collection.find_one({"_id": task_id})

    def remove_task(self, task):
        pass

    def get_tasks(
        self, skip=0, limit=100, sort_by: str = "created_at", sort_direction: int = -1
    ):
        cursor = (
            self.collection.find().sort(sort_by, sort_direction).skip(skip).limit(limit)
        )
        total_tasks = self.collection.count_documents({})
        return {"tasks": list(cursor), "total_tasks": total_tasks}

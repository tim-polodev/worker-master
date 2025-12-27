import datetime
import os

import boto3
from bson import ObjectId
from bson.errors import InvalidId
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

    def get_task_by_id(self, task_id: str):
        if not task_id:
            raise ValueError("Task ID cannot be empty")
        try:
            oid = ObjectId(task_id)
        except InvalidId:
            return None
        return self.collection.find_one({"_id": oid})

    def remove_task_by_id(self, task_id: str):
        try:
            oid = ObjectId(task_id)
        except InvalidId:
            return None
        return self.collection.delete_one({"_id": oid})

    def get_tasks(self, skip=0, limit=100, sort_by: str = "created_at", sort_direction: int = -1):
        cursor = self.collection.find().sort(sort_by, sort_direction).skip(skip).limit(limit)
        total_tasks = self.collection.count_documents({})
        return {"tasks": list(cursor), "total_tasks": total_tasks}

    def start_ecs_task(self, task_id):
        """
        Starts a Fargate task and passes the task_id as an environment variable.
        """
        ecs_client = boto3.client("ecs", region_name=os.getenv("AWS_REGION", "us-east-1"))

        response = ecs_client.run_task(
            cluster=os.getenv("ECS_CLUSTER_NAME"),
            taskDefinition=os.getenv("ECS_TASK_DEFINITION"),
            launchType="FARGATE",
            count=1,
            platformVersion="LATEST",
            networkConfiguration={
                "awsvpcConfiguration": {
                    "subnets": os.getenv("ECS_SUBNET_IDS", "").split(","),
                    "securityGroups": os.getenv("ECS_SECURITY_GROUP_IDS", "").split(","),
                    "assignPublicIp": "DISABLED",
                }
            },
            overrides={
                "containerOverrides": [
                    {
                        "name": os.getenv("ECS_CONTAINER_NAME", "worker-container"),
                        "environment": [{"name": "TASK_ID", "value": str(task_id)}],
                    }
                ]
            },
        )
        return response

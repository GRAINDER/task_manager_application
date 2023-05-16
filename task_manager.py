from pymongo import MongoClient
from pymongo.database import Database
from typing import List, Dict, Any
from pymongo.collection import Collection

def get_database() -> Database:
    client = MongoClient('mongodb://localhost:27017/')
    return client['task_manager']


def add_task(task: Dict[str, Any]) -> str:
    db = get_database()
    collection = db['tasks']
    result = collection.insert_one(task)
    return str(result.inserted_id)

def view_all_tasks() -> List[Dict[str, Any]]:
    db = get_database()
    collection = db['tasks']
    return list(collection.find())

def update_task_status(task_id: str, status: str) -> int:
    db = get_database()
    collection = db['tasks']
    result = collection.update_one({'_id': task_id}, {'$set': {'status': status}})
    return result.modified_count

def delete_task(task_id: str) -> int:
    db = get_database()
    collection = db['tasks']
    result = collection.delete_one({'_id': task_id})
    return result.deleted_count
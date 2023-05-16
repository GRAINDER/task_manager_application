import unittest
from pymongo import MongoClient
from task_manager import (
    add_task,
    view_all_tasks,
    update_task_status,
    delete_task
)

class TaskManagerTests(unittest.TestCase):
    def setUp(self):
        # Set up a test database and collection
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['test_task_manager']
        self.collection = self.db['test_tasks']

    def tearDown(self):
        # Clean up the test database and collection
        self.client.drop_database('test_task_manager')

    def test_add_task(self):
        task = {'title': 'Test Task', 'status': 'pending'}
        task_id = add_task(task)
        self.assertIsInstance(task_id, str)
        self.assertGreater(len(task_id), 0)

    def test_view_all_tasks(self):
        task1 = {'title': 'Task 1', 'status': 'pending'}
        task2 = {'title': 'Task 2', 'status': 'completed'}
        self.collection.insert_many([task1, task2])
        tasks = view_all_tasks()
        self.assertIsInstance(tasks, list)
        self.assertEqual(len(tasks), 2)

    def test_update_task_status(self):
        task = {'title': 'Test Task', 'status': 'pending'}
        task_id = add_task(task)
        modified_count = update_task_status(task_id, 'completed')
        self.assertEqual(modified_count, 1)
        updated_task = self.collection.find_one({'_id': task_id})
        self.assertEqual(updated_task['status'], 'completed')

    def test_delete_task(self):
        task = {'title': 'Test Task', 'status': 'pending'}
        task_id = add_task(task)
        deleted_count = delete_task(task_id)
        self.assertEqual(deleted_count, 1)
        task = self.collection.find_one({'_id': task_id})
        self.assertIsNone(task)
        
        #a
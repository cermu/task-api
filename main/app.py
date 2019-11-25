from flask import Blueprint
from flask_restful import Api
from resources.SystemCheck import SystemCheck
from resources.TaskListCreate import TaskListCreate, SpecificTask

api_bp = Blueprint('api_bp', __name__)
api = Api(api_bp)

# Route
api.add_resource(SystemCheck, '/system-check/')
api.add_resource(TaskListCreate, '/tasks/')
api.add_resource(SpecificTask, '/task/<int:task_id>/', endpoint='task')

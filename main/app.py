from flask import Blueprint
from flask_restful import Api
from resources.SystemCheck import SystemCheck
from resources.ListCreateTask import ListCreateTask
from resources.GetUpdateDeleteTask import GetUpdateDeleteTask

api_bp = Blueprint('api_bp', __name__)
api = Api(api_bp)

# Route
api.add_resource(SystemCheck, '/system-check/')
api.add_resource(ListCreateTask, '/tasks/', '/tasks', endpoint='tasks')
api.add_resource(GetUpdateDeleteTask, '/task/<int:task_id>/', endpoint='task')

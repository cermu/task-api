from flask import request
from flask_restful import Resource
from data.models import db, Task, TaskSchema


tasks_schema = TaskSchema(many=True)
task_schema = TaskSchema()


class TaskListCreate(Resource):
    def get(self):
        tasks = Task.query.all()
        # tasks = tasks_schema.dump(tasks).data
        # print(request.url)
        tasks = tasks_schema.dump(tasks)
        return {'status': 'success', 'results': tasks}, 200

    def post(self):
        request_data = request.get_json(force=True)
        # print(request_data)
        if not request_data:
            return {'message': 'post body required'}, 400

        # validate input
        errors = task_schema.validate(request_data)
        # print(errors)
        if errors:
            return errors, 400

        task = Task.query.filter_by(name=request_data['name']).first()
        if task:
            return {'message': 'A task with name {} already exists'.format(request_data['name'])}, 400

        new_task = Task(**request_data)
        db.session.add(new_task)
        db.session.commit()

        result = task_schema.dump(new_task)

        return result, 201


class SpecificTask(Resource):
    def get(self, task_id):
        # print(task_id)
        task = Task.query.get(task_id)
        if task:
            result = task_schema.dump(task)

            return result

        return {'message': 'task not found'}, 404

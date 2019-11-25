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
            return errors, 422

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
        if not task:
            return {'message': 'task not found'}, 404

        result = task_schema.dump(task)

        return result

    def put(self, task_id):
        update_data = request.get_json(force=True)
        if not update_data:
            return {'message': 'no data passed to update'}, 400

        # validate input
        errors = task_schema.validate(update_data)
        if errors:
            return errors, 422

        task = Task.query.get(task_id)
        if not task:
            return {'message': 'task not found'}, 404

        # check if name already exists
        if Task.query.filter_by(name=update_data['name']).first():
            return {'message': 'A task with name {} already exists'.format(update_data['name'])}, 400

        task.name = update_data['name']
        task.description = update_data['description']
        db.session.commit()

        result = task_schema.dump(task)

        return {'status': 'success', 'results': result}, 200

    def delete(self, task_id):
        task = Task.query.get(task_id)
        if not task:
            return {'message': 'task not found'}, 404

        Task.query.filter_by(id=task_id).delete()
        db.session.commit()

        return {'message': 'task deleted'}, 200

from flask import request
from flask_restful import Resource
from data.models import db, Task, TaskSchema


task_schema = TaskSchema()


class GetUpdateDeleteTask(Resource):
    def get(self, task_id):
        # check if task exists
        task = Task.query.get(task_id)
        if not task:
            return {'message': 'task not found'}, 404

        # serialize the task
        result = task_schema.dump(task)

        return result

    def put(self, task_id):
        update_data = request.get_json(force=True)

        # validate the input data
        if not update_data:
            return {'message': 'no data passed to update'}, 400

        # validate input
        errors = task_schema.validate(update_data)
        if errors:
            return errors, 422

        # check if task exists
        task = Task.query.get(task_id)
        if not task:
            return {'message': 'task not found'}, 404

        # check if name already exists
        if Task.query.filter_by(name=update_data['name']).first():
            return {'message': 'A task with name {} already exists'.format(update_data['name'])}, 400

        # update the found task
        task.name = update_data['name']
        task.description = update_data['description']
        db.session.commit()

        # serialize the task
        result = task_schema.dump(task)

        return {'message': 'success', 'results': result}, 200

    def delete(self, task_id):
        task = Task.query.get(task_id)

        # check if task exists
        if not task:
            return {'message': 'task not found'}, 404

        # delete the found task
        Task.query.filter_by(id=task_id).delete()
        db.session.commit()

        return {'message': 'task deleted'}, 200

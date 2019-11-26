from flask import request, url_for
from flask_restful import Resource
from data.models import db, Task, TaskSchema


tasks_schema = TaskSchema(many=True)
task_schema = TaskSchema()


class TaskListCreate(Resource):
    def get(self):
        args = request.args
        if args:
            # print(args.get('page'))
            page = args.get('page', 1, type=int)
            resp = Task.query.paginate(page, 2, False)
            count = len(Task.query.all())
            print(request.url)
            # print(resp.has_next)
            # print(list(resp.items))
            results = tasks_schema.dump(resp.items)
            next_url = url_for('api_bp.tasks', page=resp.next_num) \
                if resp.has_next else None

            prev_url = url_for('api_bp.tasks', page=resp.prev_num) \
                if resp.has_prev else None

            return {'count': count, 'next': next_url, 'prev': prev_url, 'results': results}

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

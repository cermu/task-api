from flask import request, url_for
from flask_restful import Resource
from data.models import db, Task, TaskSchema
from utils.settings import API_ITEMS_PER_PAGE


tasks_schema = TaskSchema(many=True)
task_schema = TaskSchema()


class ListCreateTask(Resource):
    def get(self):
        # Get the total count of tasks
        count = len(Task.query.all())

        # Get the page parameter from URL if present
        args = request.args
        if args:
            page = args.get('page', 1, type=int)

            # Returns API_ITEMS_PER_PAGE items per page
            # W3rd arg sets error_out to false
            paginated_tasks = Task.query.paginate(page, API_ITEMS_PER_PAGE, False)

            # serializing the Task items
            results = tasks_schema.dump(paginated_tasks.items)

            """
            Getting the next and previous urls by checking and setting the next and previous page num
            has_next ==> True if next page exists
            has_prev ==> True if previous page exists
            next_num ==> number of the next page
            prev_num ==> number of thr previous page
            """
            next_url = url_for('api_bp.tasks', page=paginated_tasks.next_num) \
                if paginated_tasks.has_next else None

            prev_url = url_for('api_bp.tasks', page=paginated_tasks.prev_num) \
                if paginated_tasks.has_prev else None

            # Getting the total number of pages
            total_pages = paginated_tasks.pages

            return {'count': count, 'pages': total_pages, 'next': next_url, 'prev': prev_url, 'results': results}, 200

        """
        If no page arg present in the URL,
        set the default page to 1 and paginate the results
        """
        page = 1
        tasks = Task.query.paginate(page, API_ITEMS_PER_PAGE, False)
        # serializing the Tasks
        results = tasks_schema.dump(tasks.items)

        next_url = url_for('api_bp.tasks', page=tasks.next_num) \
            if tasks.has_next else None

        prev_url = url_for('api_bp.tasks', page=tasks.prev_num) \
            if tasks.has_prev else None

        total_pages = tasks.pages

        return {'count': count, 'pages': total_pages, 'next': next_url, 'prev': prev_url, 'results': results}, 200

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


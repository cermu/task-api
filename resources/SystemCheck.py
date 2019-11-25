from flask_restful import Resource


class SystemCheck(Resource):
    def get(self):
        return {'responseCode': 0, 'responseDesc': 'system is ok'}

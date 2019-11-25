import datetime
from marshmallow import fields
from marshmallow.validate import Length
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy


ma = Marshmallow()
db = SQLAlchemy()


class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    description = db.Column(db.String(300), default='', nullable=False)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(),
                           nullable=False)
    updated_at = db.Column(db.DateTime, onupdate=datetime.datetime.utcnow)

    def __init__(self, name, description):
        self.name = name
        self.description = description


class TaskSchema(ma.Schema):
    id = fields.Integer()
    name = fields.String(required=True, validate=Length(max=20))
    description = fields.String(required=True, validate=Length(max=300))
    created_at = fields.DateTime(required=False)
    updated_at = fields.DateTime(required=False)

from app import ma, db
from app.models.task import Task
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

class TaskSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Task
        load_instance = True
        sqla_session = db.session
        include_fk = True

task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)
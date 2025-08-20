from app import ma, db
from app.models.client import Client
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

class ClientSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Client
        load_instance = True
        sqla_session = db.session
        include_fk = True

client_schema = ClientSchema()
clients_schema = ClientSchema(many=True)
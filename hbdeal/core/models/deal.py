from .db import db

class User(db.Document):
    name = db.StringField(required=True, unique=True)
    hb_token = db.StringField()
    hb_api_key = db.StringField()


class Deal(db.Document):
    user = db.ReferenceField(User, required=True)
    deal_id = db.IntField(required=True, unique=True)
    name = db.StringField(required=True)
    stage = db.StringField()
    close_date = db.DateTimeField()
    amount = db.IntField()
    # type = db.StringField(required=True)
    
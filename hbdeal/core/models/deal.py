from .db import db

class User(db.Document):
    name = db.StringField(required=True, unique=True)
    hb_client_id = db.StringField(required=True, unique=True)
    hb_client_secret = db.StringField(required=True, unique=True)
    hb_token = db.StringField()
    hb_refresh_token = db.StringField()
    hb_token_expire_date = db.DateField()


class Deal(db.Document):
    user = db.ReferenceField(User, required=True)
    deal_id = db.IntField(required=True, unique=True)
    name = db.StringField(required=True)
    stage = db.StringField()
    close_date = db.DateTimeField()
    amount = db.IntField()
    deal_type = db.StringField()
    
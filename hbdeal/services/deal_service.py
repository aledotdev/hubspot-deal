from datetime import datetime

from hbdeal.core.models.deal import Deal, User
from hbdeal.core.hb_api import HBDealApi


def create_or_update_user(user_id, name, hb_client_id, hb_client_secret):
    if user_id:
        user = get_user(user_id)
    else:
        user = User()
    
    user.name = name
    user.hb_client_id = hb_client_id
    user.hb_client_secret = hb_client_secret
    user.save()

    return user


def get_user(user_id):
    return User.objects.get(id=user_id)


def get_user_list():
    return [user for user in User.objects.all()]


def get_user_hb_api_token(user):
    token = user.hb_token
    if not token:
        token = get_new_hb_token(user)
    else:
        now = datetime.now()
        if user.hb_token_expire_date < now:
            token = refresh_hb_token(refresh_token)


def get_new_hb_token(client_id, redirect_uri):
    pass


def refresh_hb_token(refresh_token):
    pass


def update_last_deals(user):
    hb_token = get_user_hb_api_token(user)

    for deal in HBDealApi(hb_token).get_deals():
        Deal(user=user, **deal).save()


def get_user_deals(user):
    deals = Deal.objects.filter(user=user)
    return deals

      
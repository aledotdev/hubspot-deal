from datetime import datetime, timedelta

from hbdeal.core.models.deal import Deal, User
from hbdeal.core.hb_api import HBDealApi, HBOauthApi, HBEmptyApiTokenError


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


def get_user_hb_api_auth_url(user):
    oauth_api = HBOauthApi()
    return oauth_api.get_auth_url(user.hb_client_id, state=user.id)


def update_user_hb_token(user, code=None, refresh_token=None):
    oauth_api = HBOauthApi()
    data = oauth_api.update_token(user.hb_client_id, user.hb_client_secret, code=code, refresh_token=refresh_token)
    user.hb_token = data['access_token']
    user.hb_refresh_token = data['refresh_token']
    user.hb_token_expire_date = datetime.now() + timedelta(seconds=int(data['expires_in']))
    user.save()


def get_user_hb_api_token(user):
    token = user.hb_token
    if not token:
        raise HBEmptyApiTokenError

    now = datetime.now()
    if user.hb_token_expire_date < now:
        token = update_user_hb_token(user, refresh_token=user.hb_refresh_token)
    
    return token


def update_last_deals(user):
    hb_token = get_user_hb_api_token(user)

    for deal_data in HBDealApi(hb_token).get_deals():
        deal = Deal.objects.filter(user=user, deal_id=deal_data['deal_id']).first()
        if not deal:
            deal = Deal(user=user, deal_id=deal_data['deal_id'])
        
        deal.name = deal_data['name']
        deal.stage = deal_data['stage']
        deal.deal_type = deal_data['deal_type']
        deal.close_date = deal_data['close_date']
        deal.amount = deal_data['amount']
        deal.save()


def get_user_deals(user):
    deals = Deal.objects.filter(user=user)
    return deals

      
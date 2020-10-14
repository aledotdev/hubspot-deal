from hbdeal.core.models.deal import Deal, User
from hbdeal.core.hb_api import HBDealApi


def get_user_auth_hb_api(user, hb_api_class):
    if user.hb_api_key:
        return hb_api_class(api_key=user.hb_api_key)
    elif user.hb_token:
        return hb_api_class(token=user.hb_token)


def update_last_deals(user):
    deal_api = get_user_auth_hb_api(user, HBDealApi)
    for deal in deal_api.get_deals():
        Deal(user=user, **deal).save()





      
import requests
import json
from copy import copy
from datetime import datetime


SETTINGS = {
    'API_BASE_URL': 'https://api.hubapi.com',
    'OAUTH_API_GET_TOKEN_URL': 'https://api.hubapi.com/oauth/v1/token',
    'SCOPE': 'contacts',
    'OAUTH_AUTHORIZE_URL': 'https://app.hubspot.com/oauth/authorize',
    'OAUTH_REDIRECT_URL': None
}


def configure(**kwargs):
    SETTINGS.update(kwargs)


def appinit(app):
    configure(OAUTH_REDIRECT_URL=app.config['HB_OAUTH_REDIRECT_URL'])



class HBApiError(Exception):
    pass


class HBApiNotFoundError(HBApiError):
    pass


class HBEmptyApiTokenError(HBApiError):
    pass


class HBApiGetTokenError(HBApiError):
    pass


class HBApiBase(object):
    """ Base class to handle Hubspot API calls """

    def __init__(self, token):
        self.__token = token
        self.__base_headers = {
            'Authorization': 'Bearer {}'.format(self.__token)
        }

    def get(self, url_path, headers=None, params=None):

        request_headers = self.base_headers
        if headers:
            request_headers.update(headers)

        if not params:
            params = {}
        
        url = '{}/{}'.format(SETTINGS['API_BASE_URL'], url_path)

        response = requests.get(url, headers=request_headers, params=params)
        print('GET request to Hubspot: {}'.format(response.url))

        if response.status_code == 404:
            raise HBApiNotFoundError("Url not found: {}".format(response.url))
        if response.status_code != 200:
            raise HBApiError("Wrong status code: {}".format(response.status_code))

        return response
    
    def get_data(self, url_path, headers=None, params=None):
        response = self.get(url_path, headers=headers, params=params)
        return response.json()

    @property
    def base_headers(self):
        headers = copy(self.__base_headers)
        return headers


class HBOauthApi(object):
    """ Class to handle OAuth flow for Hubspot API """

    def get_auth_url(self, client_id, state=None):
        """ Get Hubspot OAuth Authorization URL """
        params = {
            'client_id': client_id,
            'redirect_uri': SETTINGS['OAUTH_REDIRECT_URL'],
            'scope': SETTINGS['SCOPE']
        }

        if state:
            params['state'] = state

        request = requests.PreparedRequest()
        request.prepare_url(SETTINGS['OAUTH_AUTHORIZE_URL'], params=params)
        return request.url
    
    def update_token(self, client_id, client_secret, code=None, refresh_token=None):
        """ Refresh user token """

        params = {
            'client_id': client_id,
            'client_secret': client_secret,
        }

        if code:
            params.update({
                'code': code,
                'grant_type': 'authorization_code',
                'redirect_uri': SETTINGS['OAUTH_REDIRECT_URL']
            })  
        elif refresh_token:
            params.update({
                'refresh_token': refresh_token,
                'grant_type': 'refresh_token',
            })

        response = requests.post(SETTINGS['OAUTH_API_GET_TOKEN_URL'], data=params)

        if response.status_code != 200:
            raise HBApiGetTokenError(response.text)
        
        return response.json()


class HBDealApi(HBApiBase):
    """ API to retrieve data for Hubspot deals """

    DEALS_LIST_PATH = 'deals/v1/deal/paged'
    DEAL_PROPERTIES = [
        'dealname',
        'dealstage',
        'dealtype',
        'amount',
        'closedate',
    ]

    def get_deals(self):
        params = {'properties': self.DEAL_PROPERTIES}
        data = self.get_data(self.DEALS_LIST_PATH, params=params)

        deals = []
        for deal_data in data['deals']:
            deal = {
                'deal_id': int(deal_data['dealId']),
                'name': self._get_deal_name(deal_data),
                'stage': self._get_deal_stage(deal_data),
                'deal_type': self._get_deal_type(deal_data),
                'amount': self._get_deal_amount(deal_data),
                'close_date': self._get_deal_close_date(deal_data)
            }
            deals.append(deal)
        return deals

    def _get_property(self, deal_data, property_name):
        try:
            return deal_data['properties'][property_name]['value']
        except KeyError:
            return None

    def _get_deal_name(self, deal_data):
        return self._get_property(deal_data, 'dealname')
    
    def _get_deal_stage(self, deal_data):
        return self._get_property(deal_data, 'dealstage')
    
    def _get_deal_type(self, deal_data):
        return self._get_property(deal_data, 'dealtype')
    
    def _get_deal_amount(self, deal_data):
        amount = self._get_property(deal_data, 'amount')
        if amount is not None:
            amount = int(amount)
        return amount
    
    def _get_deal_close_date(self, deal_data):
        close_date = self._get_property(deal_data, 'closedate')
        if close_date is not None:
            close_date = datetime.fromtimestamp(int(close_date)/1000)
        return close_date

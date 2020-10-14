import requests
import json
from copy import copy
from datetime import datetime


class HBApiError(Exception):
    pass

class HBApiNotFoundError(HBApiError):
    pass

class HBApiBase(object):
    BASE_URL = 'https://api.hubapi.com'
    
    def __init__(self, api_key=None, token=None):
        self.__base_headers = {}
        self.__api_key = api_key
        self.__token = token

    def get(self, url_path, headers=None, params=None):

        request_headers = self.base_headers
        if headers:
            request_headers.update(headers)

        if not params:
            params = {}

        if self.__api_key:
            params['hapikey'] = self.__api_key
        
        url = '{}/{}'.format(self.BASE_URL, url_path)

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
        if self.__token:
            headers['Authorization'] = 'Bearer {}'.format(self.__token)
        return headers


class HBDealApi(HBApiBase):
    DEALS_LIST_PATH = 'deals/v1/deal/paged'
    DEAL_PROPERTIES = [
        'dealname',
        'dealstage',
        'amount',
        'closedate'
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
                'amount': self._get_deal_amount(deal_data),
                'close_date': self._get_deal_close_date(deal_data),
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

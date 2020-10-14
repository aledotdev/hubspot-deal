import requests
import json
from copy import copy


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
        return data['deals']
    
    def _get_deal_name(self, deal_data):
        return data['data']

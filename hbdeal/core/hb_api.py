import requests
import json


class HBApiError(Exception):
    pass

class HBApiNotFoundError(HBApiError):
    pass

class HBApiBase(object):
    BASE_URL = 'https://api.hubapi.com'
    
    def __init__(self, api_key=None, token=None):
        self.__base_headers = {}
        if api_key:
            self.__api_key = api_key
        elif token:
            self.__base_headers['Authorization'] = 'Bearer {}'.format(token)
    
    def get(self, url_path, headers={}, params={}):

        url = '{}/{}'.format(self.BASE_URL, url_path)

        self.base_headers.update(headers)
        if self.__api_key:
            params['hapikey'] = self.__api_key

        response = requests.get(url, headers=headers, params=params)
        print('GET request to Hubspot: {}'.format(response.url))

        if response.status_code == 404:
            raise HBApiNotFoundError("Url not found: {}".format(response.url))
        if response.status_code != 200:
            raise HBApiError("Wrong status code: {}".format(response.status_code))

        return response
    
    def get_data(self, url_path, headers={}, params={}):
        response = self.get(url_path, headers=params, params=params)
        return response.json()

    @property
    def base_headers(self):
        return self.__base_headers


class HBDealApi(HBApiBase):
    DEALS_LIST_PATH = 'deals/v1/deal/paged'
    DEAL_PROPERTIES = [
        'dealname',
        'dealstage',
        'amount',
        'closedate'
    ]

    def get_deals(self):
        params = {'properties': self.DEALS_LIST_PATH}
        data = self.get_data(self.DEALS_LIST_PATH, params=params)
        return data['deals']
    
    def _get_deal_name(self, deal_data):
        return data['data']




      
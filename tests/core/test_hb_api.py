import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime

from hbdeal.core import hb_api

from tests.utils.deal_list_data import DEAL_LIST_DATA


HB_BASE_URL = 'https://api.hubapi.com'


class TestHBApiBase(unittest.TestCase):

    @patch('requests.get', return_value=MagicMock(status_code=200))
    def test_request_get_with_apikey(self, requests_get_mock):
        hb_api.HBApiBase(api_key='abc123').get('test/url')
        url = '{}/test/url'.format(HB_BASE_URL)
        requests_get_mock.assert_called_with(url, headers={}, params={'hapikey': 'abc123'})
    
    @patch('requests.get', return_value=MagicMock(status_code=200))
    def test_request_get_with_token(self, requests_get_mock):
        hb_api.HBApiBase(token='abc123').get('test/url')
        url = '{}/test/url'.format(HB_BASE_URL)
        headers = {'Authorization': 'Bearer abc123'}
        requests_get_mock.assert_called_with(url, headers=headers, params={})
    
    @patch('requests.get', return_value=MagicMock(status_code=200))
    def test_request_get_with_params(self, requests_get_mock):
        hb_api.HBApiBase(api_key='abc123').get('test/url', 
                                               params={
                                                   'properties': ['foo', 'bar'], 
                                                   'num': 123, 
                                                   'str': 'abc'})
        url = '{}/test/url'.format(HB_BASE_URL)
        requests_get_mock.assert_called_with(
            url,
            headers={},
            params={
                'hapikey': 'abc123', 
                'properties': ['foo', 'bar'],
                'num': 123,
                'str': 'abc'
            }
        )
    
    @patch('requests.get', return_value=MagicMock(status_code=200))
    def test_request_get_with_headers(self, requests_get_mock):
        extra_headers = {'UserAgent': 'test-agent', 'host': 'test.com'}
        hb_api.HBApiBase(token='abc123').get('test/url', headers=extra_headers)
        url = '{}/test/url'.format(HB_BASE_URL)
        headers = {'Authorization': 'Bearer abc123', 'UserAgent': 'test-agent', 'host': 'test.com'}
        requests_get_mock.assert_called_with(url, headers=headers, params={})
    
    @patch('requests.get', return_value=MagicMock(status_code=404))
    def test_request_get_response_not_found(self, requests_get_mock):
        with self.assertRaises(hb_api.HBApiNotFoundError):
            hb_api.HBApiBase(api_key='abc123').get('test/url')
        
    @patch('requests.get', return_value=MagicMock(status_code=500))
    def test_request_get_response_error(self, requests_get_mock):
        with self.assertRaises(hb_api.HBApiError):
            hb_api.HBApiBase(api_key='abc123').get('test/url')
    
    @patch.object(hb_api.HBApiBase, 'get', return_value=MagicMock(status_code=200, json=MagicMock()))
    def test_get_data(self, get_mock):
        params = {'bar': 'foo'}
        headers = {'foo': 'bar'}
        data = hb_api.HBApiBase(api_key='abc123').get_data('test/url', params=params, headers=headers)
        get_mock.assert_called_once_with('test/url', params=params, headers=headers)
        get_mock.return_value.json.assert_called_once_with()


class HBDealApi(unittest.TestCase):

    @patch.object(hb_api.HBApiBase, 'get_data')
    def test_get_latest_deals(self, base_get_data_mock):
        DEAL_PROPERTIES = ['dealname', 'dealstage', 'amount', 'closedate']
        hb_api.HBDealApi(api_key='abc123').get_deals()
        base_get_data_mock.assert_called_once_with('deals/v1/deal/paged', params={'properties': DEAL_PROPERTIES})
    
    @patch.object(hb_api.HBApiBase, 'get_data', return_value=DEAL_LIST_DATA)
    def test_deal_list_atributes(self, base_get_data_mock):
        data = hb_api.HBDealApi(api_key='abc123').get_deals()
        expected_data = [
            {'id': 931633510, 'name': 'Example deal',  'stage': 'presentationscheduled', 'amount': 100, 
                'close_date': datetime(2019, 8, 2, 18, 58, 38, 291000)},
            {'id': 2388597042, 'name': 'Example Deal 3', 'stage': 'closedwon', 'amount': 150, 
                'close_date': datetime(2020, 7, 31, 14, 49, 18, 166000)},
            {'id': 2388605589, 'name': 'Example Deal 2', 'stage': 'contractsent', 'amount': 200, 
                'close_date': datetime(2020, 7, 31, 14, 47, 49, 488000)}
        ]
        self.assertEqual(data, expected_data)
    


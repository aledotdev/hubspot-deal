import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime

from hbdeal.core import hb_api

from tests.utils.deal_list_data import DEAL_LIST_DATA


HB_BASE_URL = 'https://api.hubapi.com'


class TestHBApiBase(unittest.TestCase):
    
    @patch('requests.get', return_value=MagicMock(status_code=200))
    def test_request_get_with_token(self, requests_get_mock):
        hb_api.HBApiBase('abc123').get('test/url')
        requests_get_mock.assert_called_with(
            '{}/test/url'.format(HB_BASE_URL),
            headers={'Authorization': 'Bearer abc123'},
            params={}
        )
    
    @patch('requests.get', return_value=MagicMock(status_code=200))
    def test_request_get_with_params(self, requests_get_mock):
        hb_api.HBApiBase('abc123').get(
            'test/url',
            params={'properties': ['foo', 'bar'], 'num': 123, 'str': 'abc'}
        )
        requests_get_mock.assert_called_with(
            '{}/test/url'.format(HB_BASE_URL),
            headers={'Authorization': 'Bearer abc123'},
            params={'properties': ['foo', 'bar'], 'num': 123, 'str': 'abc'}
        )
    
    @patch('requests.get', return_value=MagicMock(status_code=200))
    def test_request_get_with_headers(self, requests_get_mock):
        extra_headers = {'UserAgent': 'test-agent', 'host': 'test.com'}
        hb_api.HBApiBase('abc123').get('test/url', headers=extra_headers)
        requests_get_mock.assert_called_with(
            '{}/test/url'.format(HB_BASE_URL),
            headers={'Authorization': 'Bearer abc123', 'UserAgent': 'test-agent', 'host': 'test.com'},
            params={}
        )
    
    @patch('requests.get', return_value=MagicMock(status_code=404))
    def test_request_get_response_not_found(self, requests_get_mock):
        with self.assertRaises(hb_api.HBApiNotFoundError):
            hb_api.HBApiBase('abc123').get('test/url')
        
    @patch('requests.get', return_value=MagicMock(status_code=500))
    def test_request_get_response_error(self, requests_get_mock):
        with self.assertRaises(hb_api.HBApiError):
            hb_api.HBApiBase('abc123').get('test/url')
    
    @patch.object(hb_api.HBApiBase, 'get', return_value=MagicMock(status_code=200, json=MagicMock()))
    def test_get_data(self, get_mock):
        params = {'bar': 'foo'}
        headers = {'foo': 'bar'}
        data = hb_api.HBApiBase('abc123').get_data('test/url', params=params, headers=headers)
        get_mock.assert_called_once_with('test/url', params=params, headers=headers)
        get_mock.return_value.json.assert_called_once_with()


class HBDealApi(unittest.TestCase):

    @patch.object(hb_api.HBApiBase, 'get_data')
    def test_get_latest_deals(self, base_get_data_mock):
        DEAL_PROPERTIES = ['dealname', 'dealstage', 'dealtype', 'amount', 'closedate']
        hb_api.HBDealApi('abc123').get_deals()
        base_get_data_mock.assert_called_once_with('deals/v1/deal/paged', params={'properties': DEAL_PROPERTIES})
    
    @patch.object(hb_api.HBApiBase, 'get_data', return_value=DEAL_LIST_DATA)
    def test_deal_list_atributes(self, base_get_data_mock):
        data = hb_api.HBDealApi('abc123').get_deals()
        expected_data = [
            {'deal_id': 1000000, 'name': 'deal 1',  'stage': 'stage 1', 'deal_type': 'type 1',
                'amount': 100, 'close_date': datetime(2001, 1, 1, 1, 1, 1, )},
            {'deal_id': 2000000, 'name': 'deal 2',  'stage': 'stage 2', 'deal_type': 'type 2',
                'amount': 200, 'close_date': datetime(2002, 2, 2, 2, 2, 2)},
            {'deal_id': 3000000, 'name': 'deal 3',  'stage': 'stage 3', 'deal_type': 'type 3',
                'amount': 300, 'close_date': datetime(2003, 3, 3, 3, 3, 3)},
            
        ]
        self.assertEqual(data, expected_data)
    


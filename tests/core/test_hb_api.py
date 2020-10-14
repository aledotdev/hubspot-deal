import unittest
from unittest.mock import patch, Mock

from hbdeal.core import hb_api


HB_BASE_URL = 'https://api.hubapi.com'
EMPTY_SUCCESS_RESPONSE = Mock(status_code=200)


class TestHBApiBase(unittest.TestCase):

    @patch('requests.get', return_value=EMPTY_SUCCESS_RESPONSE)
    def test_request_get_with_apikey(self, requests_get_mock):
        hb_api.HBApiBase(api_key='abc123').get('test/url')
        url = '{}/test/url'.format(HB_BASE_URL)
        requests_get_mock.assert_called_with(
            url, headers={}, params={'hapikey': 'abc123'})
        
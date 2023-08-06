import json
import unittest

from lakey_finicity.models.account.account_ach_details import AccountAchDetails


EXAMPLE_ACCOUNT_DETAIL_RESPONSE = '''
{
  "routingNumber": "123456789",
  "realAccountNumber": "002345678901"
}
'''


class TestAccountAchDetails(unittest.TestCase):
    def test_account_detail_response(self):
        response_dict = json.loads(EXAMPLE_ACCOUNT_DETAIL_RESPONSE)
        response = AccountAchDetails.from_dict(response_dict)
        self.assertEqual({}, response._unused_fields)

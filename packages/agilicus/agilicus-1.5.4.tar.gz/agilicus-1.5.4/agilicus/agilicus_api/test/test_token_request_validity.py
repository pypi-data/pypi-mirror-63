# coding: utf-8

"""
    Agilicus API

    Agilicus API endpoints  # noqa: E501

    The version of the OpenAPI document: 2020.03.05
    Contact: dev@agilicus.com
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import agilicus_api
from agilicus_api.models.token_request_validity import TokenRequestValidity  # noqa: E501
from agilicus_api.rest import ApiException

class TestTokenRequestValidity(unittest.TestCase):
    """TokenRequestValidity unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test TokenRequestValidity
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = agilicus_api.models.token_request_validity.TokenRequestValidity()  # noqa: E501
        if include_optional :
            return TokenRequestValidity(
                start = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                duration = 56, 
                end = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f')
            )
        else :
            return TokenRequestValidity(
        )

    def testTokenRequestValidity(self):
        """Test TokenRequestValidity"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()

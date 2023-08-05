# coding: utf-8

"""
    Agilicus API

    Agilicus API endpoints  # noqa: E501

    The version of the OpenAPI document: 2020.03.06
    Contact: dev@agilicus.com
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest

import agilicus_api
from agilicus_api.api.tokens_api import TokensApi  # noqa: E501
from agilicus_api.rest import ApiException


class TestTokensApi(unittest.TestCase):
    """TokensApi unit test stubs"""

    def setUp(self):
        self.api = agilicus_api.api.tokens_api.TokensApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_introspect_token(self):
        """Test case for introspect_token

        Introspect a token  # noqa: E501
        """
        pass

    def test_post_creator(self):
        """Test case for post_creator

        Create a token  # noqa: E501
        """
        pass

    def test_query_tokens(self):
        """Test case for query_tokens

        Query tokens  # noqa: E501
        """
        pass

    def test_revoke_token(self):
        """Test case for revoke_token

        Revoke a token  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()

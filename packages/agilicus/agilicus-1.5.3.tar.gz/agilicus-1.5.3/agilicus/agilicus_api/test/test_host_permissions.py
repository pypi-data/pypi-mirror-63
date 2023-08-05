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
from agilicus_api.models.host_permissions import HostPermissions  # noqa: E501
from agilicus_api.rest import ApiException

class TestHostPermissions(unittest.TestCase):
    """HostPermissions unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test HostPermissions
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = agilicus_api.models.host_permissions.HostPermissions()  # noqa: E501
        if include_optional :
            return HostPermissions(
                upstream_host = '0', 
                app_id = '123', 
                admin_org_id = '123', 
                allowed_list = [
                    agilicus_api.models.host_permissions_allowed_list.HostPermissionsAllowedList(
                        methods = [
                            'GET'
                            ], 
                        paths = [
                            '0'
                            ], 
                        query_parameters = [
                            agilicus_api.models.host_permissions_query_parameters.HostPermissionsQueryParameters(
                                name = '0', 
                                exact_match = '0', )
                            ], 
                        body = agilicus_api.models.rule_body.RuleBody(
                            json = [
                                agilicus_api.models.rule_body_json.RuleBodyJson(
                                    name = '0', 
                                    exact_match = '0', 
                                    match_type = 'string', 
                                    pointer = '/foo/0/a~1b/2', )
                                ], ), )
                    ]
            )
        else :
            return HostPermissions(
        )

    def testHostPermissions(self):
        """Test HostPermissions"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()

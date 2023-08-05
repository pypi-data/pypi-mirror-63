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
from agilicus_api.models.application_assignment import ApplicationAssignment  # noqa: E501
from agilicus_api.rest import ApiException

class TestApplicationAssignment(unittest.TestCase):
    """ApplicationAssignment unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test ApplicationAssignment
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = agilicus_api.models.application_assignment.ApplicationAssignment()  # noqa: E501
        if include_optional :
            return ApplicationAssignment(
                id = '0', 
                org_id = 'asd901laskbh', 
                environment_name = 'production', 
                application_name = 'Blogs'
            )
        else :
            return ApplicationAssignment(
                org_id = 'asd901laskbh',
                environment_name = 'production',
        )

    def testApplicationAssignment(self):
        """Test ApplicationAssignment"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()

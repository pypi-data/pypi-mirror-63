# coding: utf-8

"""
    Agilicus API

    Agilicus API endpoints  # noqa: E501

    The version of the OpenAPI document: 2020.03.06
    Contact: dev@agilicus.com
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from agilicus_api.configuration import Configuration


class ApplicationServiceAssignment(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'app_id': 'str',
        'environment_name': 'str',
        'org_id': 'str'
    }

    attribute_map = {
        'app_id': 'app_id',
        'environment_name': 'environment_name',
        'org_id': 'org_id'
    }

    def __init__(self, app_id=None, environment_name=None, org_id=None, local_vars_configuration=None):  # noqa: E501
        """ApplicationServiceAssignment - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._app_id = None
        self._environment_name = None
        self._org_id = None
        self.discriminator = None

        self.app_id = app_id
        self.environment_name = environment_name
        self.org_id = org_id

    @property
    def app_id(self):
        """Gets the app_id of this ApplicationServiceAssignment.  # noqa: E501

        The identifier of the Application to which this service is being assigned.   # noqa: E501

        :return: The app_id of this ApplicationServiceAssignment.  # noqa: E501
        :rtype: str
        """
        return self._app_id

    @app_id.setter
    def app_id(self, app_id):
        """Sets the app_id of this ApplicationServiceAssignment.

        The identifier of the Application to which this service is being assigned.   # noqa: E501

        :param app_id: The app_id of this ApplicationServiceAssignment.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and app_id is None:  # noqa: E501
            raise ValueError("Invalid value for `app_id`, must not be `None`")  # noqa: E501

        self._app_id = app_id

    @property
    def environment_name(self):
        """Gets the environment_name of this ApplicationServiceAssignment.  # noqa: E501

        The name of the Environment to which this ApplicationService is being assigned.   # noqa: E501

        :return: The environment_name of this ApplicationServiceAssignment.  # noqa: E501
        :rtype: str
        """
        return self._environment_name

    @environment_name.setter
    def environment_name(self, environment_name):
        """Sets the environment_name of this ApplicationServiceAssignment.

        The name of the Environment to which this ApplicationService is being assigned.   # noqa: E501

        :param environment_name: The environment_name of this ApplicationServiceAssignment.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and environment_name is None:  # noqa: E501
            raise ValueError("Invalid value for `environment_name`, must not be `None`")  # noqa: E501

        self._environment_name = environment_name

    @property
    def org_id(self):
        """Gets the org_id of this ApplicationServiceAssignment.  # noqa: E501

        The organisation owning the Application to which the ApplicationService is being assigned.   # noqa: E501

        :return: The org_id of this ApplicationServiceAssignment.  # noqa: E501
        :rtype: str
        """
        return self._org_id

    @org_id.setter
    def org_id(self, org_id):
        """Sets the org_id of this ApplicationServiceAssignment.

        The organisation owning the Application to which the ApplicationService is being assigned.   # noqa: E501

        :param org_id: The org_id of this ApplicationServiceAssignment.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and org_id is None:  # noqa: E501
            raise ValueError("Invalid value for `org_id`, must not be `None`")  # noqa: E501

        self._org_id = org_id

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, ApplicationServiceAssignment):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ApplicationServiceAssignment):
            return True

        return self.to_dict() != other.to_dict()

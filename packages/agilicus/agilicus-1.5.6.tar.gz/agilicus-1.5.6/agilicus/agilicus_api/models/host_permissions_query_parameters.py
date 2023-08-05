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


class HostPermissionsQueryParameters(object):
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
        'name': 'str',
        'exact_match': 'str'
    }

    attribute_map = {
        'name': 'name',
        'exact_match': 'exact_match'
    }

    def __init__(self, name=None, exact_match=None, local_vars_configuration=None):  # noqa: E501
        """HostPermissionsQueryParameters - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._name = None
        self._exact_match = None
        self.discriminator = None

        self.name = name
        if exact_match is not None:
            self.exact_match = exact_match

    @property
    def name(self):
        """Gets the name of this HostPermissionsQueryParameters.  # noqa: E501

        The name of the query parameter.  # noqa: E501

        :return: The name of this HostPermissionsQueryParameters.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this HostPermissionsQueryParameters.

        The name of the query parameter.  # noqa: E501

        :param name: The name of this HostPermissionsQueryParameters.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and name is None:  # noqa: E501
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def exact_match(self):
        """Gets the exact_match of this HostPermissionsQueryParameters.  # noqa: E501

        The given query parameter must exist, and must equal this.  # noqa: E501

        :return: The exact_match of this HostPermissionsQueryParameters.  # noqa: E501
        :rtype: str
        """
        return self._exact_match

    @exact_match.setter
    def exact_match(self, exact_match):
        """Sets the exact_match of this HostPermissionsQueryParameters.

        The given query parameter must exist, and must equal this.  # noqa: E501

        :param exact_match: The exact_match of this HostPermissionsQueryParameters.  # noqa: E501
        :type: str
        """

        self._exact_match = exact_match

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
        if not isinstance(other, HostPermissionsQueryParameters):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, HostPermissionsQueryParameters):
            return True

        return self.to_dict() != other.to_dict()

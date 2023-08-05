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


class GroupMemberAdd(object):
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
        'id': 'str',
        'org_id': 'str',
        'member_org_id': 'str'
    }

    attribute_map = {
        'id': 'id',
        'org_id': 'org_id',
        'member_org_id': 'member_org_id'
    }

    def __init__(self, id=None, org_id=None, member_org_id=None, local_vars_configuration=None):  # noqa: E501
        """GroupMemberAdd - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._id = None
        self._org_id = None
        self._member_org_id = None
        self.discriminator = None

        self.id = id
        self.org_id = org_id
        if member_org_id is not None:
            self.member_org_id = member_org_id

    @property
    def id(self):
        """Gets the id of this GroupMemberAdd.  # noqa: E501

        Unique identifier  # noqa: E501

        :return: The id of this GroupMemberAdd.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this GroupMemberAdd.

        Unique identifier  # noqa: E501

        :param id: The id of this GroupMemberAdd.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and id is None:  # noqa: E501
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id

    @property
    def org_id(self):
        """Gets the org_id of this GroupMemberAdd.  # noqa: E501

        Unique identifier  # noqa: E501

        :return: The org_id of this GroupMemberAdd.  # noqa: E501
        :rtype: str
        """
        return self._org_id

    @org_id.setter
    def org_id(self, org_id):
        """Sets the org_id of this GroupMemberAdd.

        Unique identifier  # noqa: E501

        :param org_id: The org_id of this GroupMemberAdd.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and org_id is None:  # noqa: E501
            raise ValueError("Invalid value for `org_id`, must not be `None`")  # noqa: E501

        self._org_id = org_id

    @property
    def member_org_id(self):
        """Gets the member_org_id of this GroupMemberAdd.  # noqa: E501

        Unique identifier  # noqa: E501

        :return: The member_org_id of this GroupMemberAdd.  # noqa: E501
        :rtype: str
        """
        return self._member_org_id

    @member_org_id.setter
    def member_org_id(self, member_org_id):
        """Sets the member_org_id of this GroupMemberAdd.

        Unique identifier  # noqa: E501

        :param member_org_id: The member_org_id of this GroupMemberAdd.  # noqa: E501
        :type: str
        """

        self._member_org_id = member_org_id

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
        if not isinstance(other, GroupMemberAdd):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, GroupMemberAdd):
            return True

        return self.to_dict() != other.to_dict()

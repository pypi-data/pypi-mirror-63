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


class HostPermissions(object):
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
        'upstream_host': 'str',
        'app_id': 'str',
        'admin_org_id': 'str',
        'allowed_list': 'list[HostPermissionsAllowedList]'
    }

    attribute_map = {
        'upstream_host': 'upstream_host',
        'app_id': 'app_id',
        'admin_org_id': 'admin_org_id',
        'allowed_list': 'allowed_list'
    }

    def __init__(self, upstream_host=None, app_id=None, admin_org_id=None, allowed_list=None, local_vars_configuration=None):  # noqa: E501
        """HostPermissions - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._upstream_host = None
        self._app_id = None
        self._admin_org_id = None
        self._allowed_list = None
        self.discriminator = None

        if upstream_host is not None:
            self.upstream_host = upstream_host
        if app_id is not None:
            self.app_id = app_id
        if admin_org_id is not None:
            self.admin_org_id = admin_org_id
        if allowed_list is not None:
            self.allowed_list = allowed_list

    @property
    def upstream_host(self):
        """Gets the upstream_host of this HostPermissions.  # noqa: E501


        :return: The upstream_host of this HostPermissions.  # noqa: E501
        :rtype: str
        """
        return self._upstream_host

    @upstream_host.setter
    def upstream_host(self, upstream_host):
        """Sets the upstream_host of this HostPermissions.


        :param upstream_host: The upstream_host of this HostPermissions.  # noqa: E501
        :type: str
        """

        self._upstream_host = upstream_host

    @property
    def app_id(self):
        """Gets the app_id of this HostPermissions.  # noqa: E501

        Unique identifier  # noqa: E501

        :return: The app_id of this HostPermissions.  # noqa: E501
        :rtype: str
        """
        return self._app_id

    @app_id.setter
    def app_id(self, app_id):
        """Sets the app_id of this HostPermissions.

        Unique identifier  # noqa: E501

        :param app_id: The app_id of this HostPermissions.  # noqa: E501
        :type: str
        """

        self._app_id = app_id

    @property
    def admin_org_id(self):
        """Gets the admin_org_id of this HostPermissions.  # noqa: E501

        Unique identifier  # noqa: E501

        :return: The admin_org_id of this HostPermissions.  # noqa: E501
        :rtype: str
        """
        return self._admin_org_id

    @admin_org_id.setter
    def admin_org_id(self, admin_org_id):
        """Sets the admin_org_id of this HostPermissions.

        Unique identifier  # noqa: E501

        :param admin_org_id: The admin_org_id of this HostPermissions.  # noqa: E501
        :type: str
        """

        self._admin_org_id = admin_org_id

    @property
    def allowed_list(self):
        """Gets the allowed_list of this HostPermissions.  # noqa: E501


        :return: The allowed_list of this HostPermissions.  # noqa: E501
        :rtype: list[HostPermissionsAllowedList]
        """
        return self._allowed_list

    @allowed_list.setter
    def allowed_list(self, allowed_list):
        """Sets the allowed_list of this HostPermissions.


        :param allowed_list: The allowed_list of this HostPermissions.  # noqa: E501
        :type: list[HostPermissionsAllowedList]
        """

        self._allowed_list = allowed_list

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
        if not isinstance(other, HostPermissions):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, HostPermissions):
            return True

        return self.to_dict() != other.to_dict()

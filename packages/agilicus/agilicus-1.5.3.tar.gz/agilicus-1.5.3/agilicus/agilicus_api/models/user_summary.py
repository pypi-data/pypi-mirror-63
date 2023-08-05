# coding: utf-8

"""
    Agilicus API

    Agilicus API endpoints  # noqa: E501

    The version of the OpenAPI document: 2020.03.05
    Contact: dev@agilicus.com
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from agilicus_api.configuration import Configuration


class UserSummary(object):
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
        'external_id': 'str',
        'enabled': 'bool',
        'first_name': 'str',
        'last_name': 'str',
        'email': 'str',
        'provider': 'str',
        'roles': 'dict(str, list[str])',
        'org_id': 'str',
        'type': 'str',
        'created': 'datetime',
        'updated': 'datetime'
    }

    attribute_map = {
        'id': 'id',
        'external_id': 'external_id',
        'enabled': 'enabled',
        'first_name': 'first_name',
        'last_name': 'last_name',
        'email': 'email',
        'provider': 'provider',
        'roles': 'roles',
        'org_id': 'org_id',
        'type': 'type',
        'created': 'created',
        'updated': 'updated'
    }

    discriminator_value_class_map = {
        
    }

    def __init__(self, id=None, external_id=None, enabled=None, first_name=None, last_name=None, email=None, provider=None, roles=None, org_id=None, type=None, created=None, updated=None, local_vars_configuration=None):  # noqa: E501
        """UserSummary - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._id = None
        self._external_id = None
        self._enabled = None
        self._first_name = None
        self._last_name = None
        self._email = None
        self._provider = None
        self._roles = None
        self._org_id = None
        self._type = None
        self._created = None
        self._updated = None
        self.discriminator = 'type'

        if id is not None:
            self.id = id
        if external_id is not None:
            self.external_id = external_id
        if enabled is not None:
            self.enabled = enabled
        if first_name is not None:
            self.first_name = first_name
        if last_name is not None:
            self.last_name = last_name
        if email is not None:
            self.email = email
        self.provider = provider
        if roles is not None:
            self.roles = roles
        if org_id is not None:
            self.org_id = org_id
        if type is not None:
            self.type = type
        if created is not None:
            self.created = created
        if updated is not None:
            self.updated = updated

    @property
    def id(self):
        """Gets the id of this UserSummary.  # noqa: E501

        Unique identifier  # noqa: E501

        :return: The id of this UserSummary.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this UserSummary.

        Unique identifier  # noqa: E501

        :param id: The id of this UserSummary.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def external_id(self):
        """Gets the external_id of this UserSummary.  # noqa: E501

        External unique identifier  # noqa: E501

        :return: The external_id of this UserSummary.  # noqa: E501
        :rtype: str
        """
        return self._external_id

    @external_id.setter
    def external_id(self, external_id):
        """Sets the external_id of this UserSummary.

        External unique identifier  # noqa: E501

        :param external_id: The external_id of this UserSummary.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                external_id is not None and len(external_id) > 100):
            raise ValueError("Invalid value for `external_id`, length must be less than or equal to `100`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                external_id is not None and len(external_id) < 1):
            raise ValueError("Invalid value for `external_id`, length must be greater than or equal to `1`")  # noqa: E501

        self._external_id = external_id

    @property
    def enabled(self):
        """Gets the enabled of this UserSummary.  # noqa: E501

        Enable/Disable a user  # noqa: E501

        :return: The enabled of this UserSummary.  # noqa: E501
        :rtype: bool
        """
        return self._enabled

    @enabled.setter
    def enabled(self, enabled):
        """Sets the enabled of this UserSummary.

        Enable/Disable a user  # noqa: E501

        :param enabled: The enabled of this UserSummary.  # noqa: E501
        :type: bool
        """

        self._enabled = enabled

    @property
    def first_name(self):
        """Gets the first_name of this UserSummary.  # noqa: E501

        User's first name  # noqa: E501

        :return: The first_name of this UserSummary.  # noqa: E501
        :rtype: str
        """
        return self._first_name

    @first_name.setter
    def first_name(self, first_name):
        """Sets the first_name of this UserSummary.

        User's first name  # noqa: E501

        :param first_name: The first_name of this UserSummary.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                first_name is not None and len(first_name) > 100):
            raise ValueError("Invalid value for `first_name`, length must be less than or equal to `100`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                first_name is not None and len(first_name) < 1):
            raise ValueError("Invalid value for `first_name`, length must be greater than or equal to `1`")  # noqa: E501

        self._first_name = first_name

    @property
    def last_name(self):
        """Gets the last_name of this UserSummary.  # noqa: E501

        User's last name  # noqa: E501

        :return: The last_name of this UserSummary.  # noqa: E501
        :rtype: str
        """
        return self._last_name

    @last_name.setter
    def last_name(self, last_name):
        """Sets the last_name of this UserSummary.

        User's last name  # noqa: E501

        :param last_name: The last_name of this UserSummary.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                last_name is not None and len(last_name) > 100):
            raise ValueError("Invalid value for `last_name`, length must be less than or equal to `100`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                last_name is not None and len(last_name) < 0):
            raise ValueError("Invalid value for `last_name`, length must be greater than or equal to `0`")  # noqa: E501

        self._last_name = last_name

    @property
    def email(self):
        """Gets the email of this UserSummary.  # noqa: E501

        User's email-addr  # noqa: E501

        :return: The email of this UserSummary.  # noqa: E501
        :rtype: str
        """
        return self._email

    @email.setter
    def email(self, email):
        """Sets the email of this UserSummary.

        User's email-addr  # noqa: E501

        :param email: The email of this UserSummary.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                email is not None and len(email) > 100):
            raise ValueError("Invalid value for `email`, length must be less than or equal to `100`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                email is not None and len(email) < 1):
            raise ValueError("Invalid value for `email`, length must be greater than or equal to `1`")  # noqa: E501

        self._email = email

    @property
    def provider(self):
        """Gets the provider of this UserSummary.  # noqa: E501

        Upstream IdP name  # noqa: E501

        :return: The provider of this UserSummary.  # noqa: E501
        :rtype: str
        """
        return self._provider

    @provider.setter
    def provider(self, provider):
        """Sets the provider of this UserSummary.

        Upstream IdP name  # noqa: E501

        :param provider: The provider of this UserSummary.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                provider is not None and len(provider) > 100):
            raise ValueError("Invalid value for `provider`, length must be less than or equal to `100`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                provider is not None and len(provider) < 1):
            raise ValueError("Invalid value for `provider`, length must be greater than or equal to `1`")  # noqa: E501

        self._provider = provider

    @property
    def roles(self):
        """Gets the roles of this UserSummary.  # noqa: E501


        :return: The roles of this UserSummary.  # noqa: E501
        :rtype: dict(str, list[str])
        """
        return self._roles

    @roles.setter
    def roles(self, roles):
        """Sets the roles of this UserSummary.


        :param roles: The roles of this UserSummary.  # noqa: E501
        :type: dict(str, list[str])
        """

        self._roles = roles

    @property
    def org_id(self):
        """Gets the org_id of this UserSummary.  # noqa: E501

        Unique identifier  # noqa: E501

        :return: The org_id of this UserSummary.  # noqa: E501
        :rtype: str
        """
        return self._org_id

    @org_id.setter
    def org_id(self, org_id):
        """Sets the org_id of this UserSummary.

        Unique identifier  # noqa: E501

        :param org_id: The org_id of this UserSummary.  # noqa: E501
        :type: str
        """

        self._org_id = org_id

    @property
    def type(self):
        """Gets the type of this UserSummary.  # noqa: E501


        :return: The type of this UserSummary.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this UserSummary.


        :param type: The type of this UserSummary.  # noqa: E501
        :type: str
        """
        allowed_values = ["user", "group", "sysgroup", "bigroup"]  # noqa: E501
        if self.local_vars_configuration.client_side_validation and type not in allowed_values:  # noqa: E501
            raise ValueError(
                "Invalid value for `type` ({0}), must be one of {1}"  # noqa: E501
                .format(type, allowed_values)
            )

        self._type = type

    @property
    def created(self):
        """Gets the created of this UserSummary.  # noqa: E501

        Creation time  # noqa: E501

        :return: The created of this UserSummary.  # noqa: E501
        :rtype: datetime
        """
        return self._created

    @created.setter
    def created(self, created):
        """Sets the created of this UserSummary.

        Creation time  # noqa: E501

        :param created: The created of this UserSummary.  # noqa: E501
        :type: datetime
        """

        self._created = created

    @property
    def updated(self):
        """Gets the updated of this UserSummary.  # noqa: E501

        Update time  # noqa: E501

        :return: The updated of this UserSummary.  # noqa: E501
        :rtype: datetime
        """
        return self._updated

    @updated.setter
    def updated(self, updated):
        """Sets the updated of this UserSummary.

        Update time  # noqa: E501

        :param updated: The updated of this UserSummary.  # noqa: E501
        :type: datetime
        """

        self._updated = updated

    def get_real_child_model(self, data):
        """Returns the real base class specified by the discriminator"""
        discriminator_key = self.attribute_map[self.discriminator]
        discriminator_value = data[discriminator_key]
        return self.discriminator_value_class_map.get(discriminator_value)

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
        if not isinstance(other, UserSummary):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, UserSummary):
            return True

        return self.to_dict() != other.to_dict()

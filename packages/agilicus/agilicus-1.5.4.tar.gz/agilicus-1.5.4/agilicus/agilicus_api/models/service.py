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


class Service(object):
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
        'name': 'str',
        'description': 'str',
        'org_id': 'str',
        'contact_email': 'str',
        'roles': 'list[Role]',
        'definitions': 'list[Definition]',
        'base_url': 'str'
    }

    attribute_map = {
        'id': 'id',
        'name': 'name',
        'description': 'description',
        'org_id': 'org_id',
        'contact_email': 'contact_email',
        'roles': 'roles',
        'definitions': 'definitions',
        'base_url': 'base_url'
    }

    def __init__(self, id=None, name=None, description=None, org_id=None, contact_email=None, roles=None, definitions=None, base_url=None, local_vars_configuration=None):  # noqa: E501
        """Service - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._id = None
        self._name = None
        self._description = None
        self._org_id = None
        self._contact_email = None
        self._roles = None
        self._definitions = None
        self._base_url = None
        self.discriminator = None

        if id is not None:
            self.id = id
        self.name = name
        if description is not None:
            self.description = description
        self.org_id = org_id
        if contact_email is not None:
            self.contact_email = contact_email
        if roles is not None:
            self.roles = roles
        if definitions is not None:
            self.definitions = definitions
        self.base_url = base_url

    @property
    def id(self):
        """Gets the id of this Service.  # noqa: E501

        Unique identifier  # noqa: E501

        :return: The id of this Service.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Service.

        Unique identifier  # noqa: E501

        :param id: The id of this Service.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def name(self):
        """Gets the name of this Service.  # noqa: E501

        Service name. Must be unique accross all Applications and Services.  # noqa: E501

        :return: The name of this Service.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this Service.

        Service name. Must be unique accross all Applications and Services.  # noqa: E501

        :param name: The name of this Service.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and name is None:  # noqa: E501
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                name is not None and len(name) > 100):
            raise ValueError("Invalid value for `name`, length must be less than or equal to `100`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                name is not None and len(name) < 1):
            raise ValueError("Invalid value for `name`, length must be greater than or equal to `1`")  # noqa: E501

        self._name = name

    @property
    def description(self):
        """Gets the description of this Service.  # noqa: E501

        Service description text  # noqa: E501

        :return: The description of this Service.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this Service.

        Service description text  # noqa: E501

        :param description: The description of this Service.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def org_id(self):
        """Gets the org_id of this Service.  # noqa: E501

        organisation id  # noqa: E501

        :return: The org_id of this Service.  # noqa: E501
        :rtype: str
        """
        return self._org_id

    @org_id.setter
    def org_id(self, org_id):
        """Sets the org_id of this Service.

        organisation id  # noqa: E501

        :param org_id: The org_id of this Service.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and org_id is None:  # noqa: E501
            raise ValueError("Invalid value for `org_id`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                org_id is not None and len(org_id) > 40):
            raise ValueError("Invalid value for `org_id`, length must be less than or equal to `40`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                org_id is not None and len(org_id) < 1):
            raise ValueError("Invalid value for `org_id`, length must be greater than or equal to `1`")  # noqa: E501

        self._org_id = org_id

    @property
    def contact_email(self):
        """Gets the contact_email of this Service.  # noqa: E501

        Administrator contact email  # noqa: E501

        :return: The contact_email of this Service.  # noqa: E501
        :rtype: str
        """
        return self._contact_email

    @contact_email.setter
    def contact_email(self, contact_email):
        """Sets the contact_email of this Service.

        Administrator contact email  # noqa: E501

        :param contact_email: The contact_email of this Service.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                contact_email is not None and len(contact_email) > 100):
            raise ValueError("Invalid value for `contact_email`, length must be less than or equal to `100`")  # noqa: E501

        self._contact_email = contact_email

    @property
    def roles(self):
        """Gets the roles of this Service.  # noqa: E501


        :return: The roles of this Service.  # noqa: E501
        :rtype: list[Role]
        """
        return self._roles

    @roles.setter
    def roles(self, roles):
        """Sets the roles of this Service.


        :param roles: The roles of this Service.  # noqa: E501
        :type: list[Role]
        """

        self._roles = roles

    @property
    def definitions(self):
        """Gets the definitions of this Service.  # noqa: E501


        :return: The definitions of this Service.  # noqa: E501
        :rtype: list[Definition]
        """
        return self._definitions

    @definitions.setter
    def definitions(self, definitions):
        """Sets the definitions of this Service.


        :param definitions: The definitions of this Service.  # noqa: E501
        :type: list[Definition]
        """

        self._definitions = definitions

    @property
    def base_url(self):
        """Gets the base_url of this Service.  # noqa: E501

        The URL which forms the base of this service. This value will be joined with the paths in the rules for this service to form its authorization model.   # noqa: E501

        :return: The base_url of this Service.  # noqa: E501
        :rtype: str
        """
        return self._base_url

    @base_url.setter
    def base_url(self, base_url):
        """Sets the base_url of this Service.

        The URL which forms the base of this service. This value will be joined with the paths in the rules for this service to form its authorization model.   # noqa: E501

        :param base_url: The base_url of this Service.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and base_url is None:  # noqa: E501
            raise ValueError("Invalid value for `base_url`, must not be `None`")  # noqa: E501

        self._base_url = base_url

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
        if not isinstance(other, Service):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, Service):
            return True

        return self.to_dict() != other.to_dict()

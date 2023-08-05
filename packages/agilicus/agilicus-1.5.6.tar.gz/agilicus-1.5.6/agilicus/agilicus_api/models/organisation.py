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


class Organisation(object):
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
        'all_users_group_id': 'str',
        'all_users_all_suborgs_group_id': 'str',
        'all_users_direct_suborgs_group_id': 'str',
        'external_id': 'str',
        'organisation': 'str',
        'issuer': 'str',
        'subdomain': 'str',
        'created': 'datetime',
        'updated': 'datetime',
        'contact_id': 'str',
        'parent_id': 'str',
        'root_org_id': 'str',
        'auto_create': 'bool'
    }

    attribute_map = {
        'id': 'id',
        'all_users_group_id': 'all_users_group_id',
        'all_users_all_suborgs_group_id': 'all_users_all_suborgs_group_id',
        'all_users_direct_suborgs_group_id': 'all_users_direct_suborgs_group_id',
        'external_id': 'external_id',
        'organisation': 'organisation',
        'issuer': 'issuer',
        'subdomain': 'subdomain',
        'created': 'created',
        'updated': 'updated',
        'contact_id': 'contact_id',
        'parent_id': 'parent_id',
        'root_org_id': 'root_org_id',
        'auto_create': 'auto_create'
    }

    def __init__(self, id=None, all_users_group_id=None, all_users_all_suborgs_group_id=None, all_users_direct_suborgs_group_id=None, external_id=None, organisation=None, issuer=None, subdomain=None, created=None, updated=None, contact_id=None, parent_id=None, root_org_id=None, auto_create=True, local_vars_configuration=None):  # noqa: E501
        """Organisation - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._id = None
        self._all_users_group_id = None
        self._all_users_all_suborgs_group_id = None
        self._all_users_direct_suborgs_group_id = None
        self._external_id = None
        self._organisation = None
        self._issuer = None
        self._subdomain = None
        self._created = None
        self._updated = None
        self._contact_id = None
        self._parent_id = None
        self._root_org_id = None
        self._auto_create = None
        self.discriminator = None

        if id is not None:
            self.id = id
        if all_users_group_id is not None:
            self.all_users_group_id = all_users_group_id
        if all_users_all_suborgs_group_id is not None:
            self.all_users_all_suborgs_group_id = all_users_all_suborgs_group_id
        if all_users_direct_suborgs_group_id is not None:
            self.all_users_direct_suborgs_group_id = all_users_direct_suborgs_group_id
        if external_id is not None:
            self.external_id = external_id
        if organisation is not None:
            self.organisation = organisation
        if issuer is not None:
            self.issuer = issuer
        if subdomain is not None:
            self.subdomain = subdomain
        if created is not None:
            self.created = created
        if updated is not None:
            self.updated = updated
        if contact_id is not None:
            self.contact_id = contact_id
        if parent_id is not None:
            self.parent_id = parent_id
        if root_org_id is not None:
            self.root_org_id = root_org_id
        if auto_create is not None:
            self.auto_create = auto_create

    @property
    def id(self):
        """Gets the id of this Organisation.  # noqa: E501

        Unique identifier  # noqa: E501

        :return: The id of this Organisation.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Organisation.

        Unique identifier  # noqa: E501

        :param id: The id of this Organisation.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def all_users_group_id(self):
        """Gets the all_users_group_id of this Organisation.  # noqa: E501

        group id of group containing this organisations all users  # noqa: E501

        :return: The all_users_group_id of this Organisation.  # noqa: E501
        :rtype: str
        """
        return self._all_users_group_id

    @all_users_group_id.setter
    def all_users_group_id(self, all_users_group_id):
        """Sets the all_users_group_id of this Organisation.

        group id of group containing this organisations all users  # noqa: E501

        :param all_users_group_id: The all_users_group_id of this Organisation.  # noqa: E501
        :type: str
        """

        self._all_users_group_id = all_users_group_id

    @property
    def all_users_all_suborgs_group_id(self):
        """Gets the all_users_all_suborgs_group_id of this Organisation.  # noqa: E501

        group id of group containing this organisations all users including all sub organisations  # noqa: E501

        :return: The all_users_all_suborgs_group_id of this Organisation.  # noqa: E501
        :rtype: str
        """
        return self._all_users_all_suborgs_group_id

    @all_users_all_suborgs_group_id.setter
    def all_users_all_suborgs_group_id(self, all_users_all_suborgs_group_id):
        """Sets the all_users_all_suborgs_group_id of this Organisation.

        group id of group containing this organisations all users including all sub organisations  # noqa: E501

        :param all_users_all_suborgs_group_id: The all_users_all_suborgs_group_id of this Organisation.  # noqa: E501
        :type: str
        """

        self._all_users_all_suborgs_group_id = all_users_all_suborgs_group_id

    @property
    def all_users_direct_suborgs_group_id(self):
        """Gets the all_users_direct_suborgs_group_id of this Organisation.  # noqa: E501

        group id of group containing this organisations all users including only direct sub organisations  # noqa: E501

        :return: The all_users_direct_suborgs_group_id of this Organisation.  # noqa: E501
        :rtype: str
        """
        return self._all_users_direct_suborgs_group_id

    @all_users_direct_suborgs_group_id.setter
    def all_users_direct_suborgs_group_id(self, all_users_direct_suborgs_group_id):
        """Sets the all_users_direct_suborgs_group_id of this Organisation.

        group id of group containing this organisations all users including only direct sub organisations  # noqa: E501

        :param all_users_direct_suborgs_group_id: The all_users_direct_suborgs_group_id of this Organisation.  # noqa: E501
        :type: str
        """

        self._all_users_direct_suborgs_group_id = all_users_direct_suborgs_group_id

    @property
    def external_id(self):
        """Gets the external_id of this Organisation.  # noqa: E501

        External unique identifier  # noqa: E501

        :return: The external_id of this Organisation.  # noqa: E501
        :rtype: str
        """
        return self._external_id

    @external_id.setter
    def external_id(self, external_id):
        """Sets the external_id of this Organisation.

        External unique identifier  # noqa: E501

        :param external_id: The external_id of this Organisation.  # noqa: E501
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
    def organisation(self):
        """Gets the organisation of this Organisation.  # noqa: E501

        organisation name  # noqa: E501

        :return: The organisation of this Organisation.  # noqa: E501
        :rtype: str
        """
        return self._organisation

    @organisation.setter
    def organisation(self, organisation):
        """Sets the organisation of this Organisation.

        organisation name  # noqa: E501

        :param organisation: The organisation of this Organisation.  # noqa: E501
        :type: str
        """

        self._organisation = organisation

    @property
    def issuer(self):
        """Gets the issuer of this Organisation.  # noqa: E501

        connect id issuer  # noqa: E501

        :return: The issuer of this Organisation.  # noqa: E501
        :rtype: str
        """
        return self._issuer

    @issuer.setter
    def issuer(self, issuer):
        """Sets the issuer of this Organisation.

        connect id issuer  # noqa: E501

        :param issuer: The issuer of this Organisation.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                issuer is not None and len(issuer) > 100):
            raise ValueError("Invalid value for `issuer`, length must be less than or equal to `100`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                issuer is not None and len(issuer) < 1):
            raise ValueError("Invalid value for `issuer`, length must be greater than or equal to `1`")  # noqa: E501

        self._issuer = issuer

    @property
    def subdomain(self):
        """Gets the subdomain of this Organisation.  # noqa: E501

        Organisations subdomain  # noqa: E501

        :return: The subdomain of this Organisation.  # noqa: E501
        :rtype: str
        """
        return self._subdomain

    @subdomain.setter
    def subdomain(self, subdomain):
        """Sets the subdomain of this Organisation.

        Organisations subdomain  # noqa: E501

        :param subdomain: The subdomain of this Organisation.  # noqa: E501
        :type: str
        """
        if (self.local_vars_configuration.client_side_validation and
                subdomain is not None and len(subdomain) > 100):
            raise ValueError("Invalid value for `subdomain`, length must be less than or equal to `100`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                subdomain is not None and len(subdomain) < 1):
            raise ValueError("Invalid value for `subdomain`, length must be greater than or equal to `1`")  # noqa: E501

        self._subdomain = subdomain

    @property
    def created(self):
        """Gets the created of this Organisation.  # noqa: E501

        Creation time  # noqa: E501

        :return: The created of this Organisation.  # noqa: E501
        :rtype: datetime
        """
        return self._created

    @created.setter
    def created(self, created):
        """Sets the created of this Organisation.

        Creation time  # noqa: E501

        :param created: The created of this Organisation.  # noqa: E501
        :type: datetime
        """

        self._created = created

    @property
    def updated(self):
        """Gets the updated of this Organisation.  # noqa: E501

        Update time  # noqa: E501

        :return: The updated of this Organisation.  # noqa: E501
        :rtype: datetime
        """
        return self._updated

    @updated.setter
    def updated(self, updated):
        """Sets the updated of this Organisation.

        Update time  # noqa: E501

        :param updated: The updated of this Organisation.  # noqa: E501
        :type: datetime
        """

        self._updated = updated

    @property
    def contact_id(self):
        """Gets the contact_id of this Organisation.  # noqa: E501

        GUID of the organisation admin  # noqa: E501

        :return: The contact_id of this Organisation.  # noqa: E501
        :rtype: str
        """
        return self._contact_id

    @contact_id.setter
    def contact_id(self, contact_id):
        """Sets the contact_id of this Organisation.

        GUID of the organisation admin  # noqa: E501

        :param contact_id: The contact_id of this Organisation.  # noqa: E501
        :type: str
        """

        self._contact_id = contact_id

    @property
    def parent_id(self):
        """Gets the parent_id of this Organisation.  # noqa: E501

        parent organisation id  # noqa: E501

        :return: The parent_id of this Organisation.  # noqa: E501
        :rtype: str
        """
        return self._parent_id

    @parent_id.setter
    def parent_id(self, parent_id):
        """Sets the parent_id of this Organisation.

        parent organisation id  # noqa: E501

        :param parent_id: The parent_id of this Organisation.  # noqa: E501
        :type: str
        """

        self._parent_id = parent_id

    @property
    def root_org_id(self):
        """Gets the root_org_id of this Organisation.  # noqa: E501

        The id of the organisation at the root of this organisation hierarchy. For example, if A is the parent of B, and B is the parent of C, then A would be the root organisation of A, B and C. Note that this field will be ignored if changed.   # noqa: E501

        :return: The root_org_id of this Organisation.  # noqa: E501
        :rtype: str
        """
        return self._root_org_id

    @root_org_id.setter
    def root_org_id(self, root_org_id):
        """Sets the root_org_id of this Organisation.

        The id of the organisation at the root of this organisation hierarchy. For example, if A is the parent of B, and B is the parent of C, then A would be the root organisation of A, B and C. Note that this field will be ignored if changed.   # noqa: E501

        :param root_org_id: The root_org_id of this Organisation.  # noqa: E501
        :type: str
        """

        self._root_org_id = root_org_id

    @property
    def auto_create(self):
        """Gets the auto_create of this Organisation.  # noqa: E501

        Auto-creates a user  # noqa: E501

        :return: The auto_create of this Organisation.  # noqa: E501
        :rtype: bool
        """
        return self._auto_create

    @auto_create.setter
    def auto_create(self, auto_create):
        """Sets the auto_create of this Organisation.

        Auto-creates a user  # noqa: E501

        :param auto_create: The auto_create of this Organisation.  # noqa: E501
        :type: bool
        """

        self._auto_create = auto_create

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
        if not isinstance(other, Organisation):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, Organisation):
            return True

        return self.to_dict() != other.to_dict()

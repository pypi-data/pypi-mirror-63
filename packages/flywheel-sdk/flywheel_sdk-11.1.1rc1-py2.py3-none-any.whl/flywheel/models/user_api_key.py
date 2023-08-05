# coding: utf-8

"""
    Flywheel

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: 11.1.1-rc.1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


## NOTE: This file is auto generated by the swagger code generator program.
## Do not edit the file manually.

import pprint
import re  # noqa: F401

import six

# NOTE: This file is auto generated by the swagger code generator program.
# Do not edit the class manually.


class UserApiKey(object):

    swagger_types = {
        'key': 'str',
        'created': 'datetime',
        'last_used': 'datetime'
    }

    attribute_map = {
        'key': 'key',
        'created': 'created',
        'last_used': 'last_used'
    }

    rattribute_map = {
        'key': 'key',
        'created': 'created',
        'last_used': 'last_used'
    }

    def __init__(self, key=None, created=None, last_used=None):  # noqa: E501
        """UserApiKey - a model defined in Swagger"""
        super(UserApiKey, self).__init__()

        self._key = None
        self._created = None
        self._last_used = None
        self.discriminator = None
        self.alt_discriminator = None

        if key is not None:
            self.key = key
        if created is not None:
            self.created = created
        if last_used is not None:
            self.last_used = last_used

    @property
    def key(self):
        """Gets the key of this UserApiKey.


        :return: The key of this UserApiKey.
        :rtype: str
        """
        return self._key

    @key.setter
    def key(self, key):
        """Sets the key of this UserApiKey.


        :param key: The key of this UserApiKey.  # noqa: E501
        :type: str
        """

        self._key = key

    @property
    def created(self):
        """Gets the created of this UserApiKey.

        Creation time (automatically set)

        :return: The created of this UserApiKey.
        :rtype: datetime
        """
        return self._created

    @created.setter
    def created(self, created):
        """Sets the created of this UserApiKey.

        Creation time (automatically set)

        :param created: The created of this UserApiKey.  # noqa: E501
        :type: datetime
        """

        self._created = created

    @property
    def last_used(self):
        """Gets the last_used of this UserApiKey.


        :return: The last_used of this UserApiKey.
        :rtype: datetime
        """
        return self._last_used

    @last_used.setter
    def last_used(self, last_used):
        """Sets the last_used of this UserApiKey.


        :param last_used: The last_used of this UserApiKey.  # noqa: E501
        :type: datetime
        """

        self._last_used = last_used


    @staticmethod
    def positional_to_model(value):
        """Converts a positional argument to a model value"""
        return value

    def return_value(self):
        """Unwraps return value from model"""
        return self

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
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
        if not isinstance(other, UserApiKey):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

    # Container emulation
    def __getitem__(self, key):
        """Returns the value of key"""
        key = self._map_key(key)
        return getattr(self, key)

    def __setitem__(self, key, value):
        """Sets the value of key"""
        key = self._map_key(key)
        setattr(self, key, value)

    def __contains__(self, key):
        """Checks if the given value is a key in this object"""
        key = self._map_key(key, raise_on_error=False)
        return key is not None

    def keys(self):
        """Returns the list of json properties in the object"""
        return self.__class__.rattribute_map.keys()

    def values(self):
        """Returns the list of values in the object"""
        for key in self.__class__.attribute_map.keys():
            yield getattr(self, key)

    def items(self):
        """Returns the list of json property to value mapping"""
        for key, prop in self.__class__.rattribute_map.items():
            yield key, getattr(self, prop)

    def get(self, key, default=None):
        """Get the value of the provided json property, or default"""
        key = self._map_key(key, raise_on_error=False)
        if key:
            return getattr(self, key, default)
        return default

    def _map_key(self, key, raise_on_error=True):
        result = self.__class__.rattribute_map.get(key)
        if result is None:
            if raise_on_error:
                raise AttributeError('Invalid attribute name: {}'.format(key))
            return None
        return '_' + result

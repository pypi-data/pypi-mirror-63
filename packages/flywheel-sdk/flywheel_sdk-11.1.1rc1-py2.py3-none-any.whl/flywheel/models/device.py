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

from flywheel.models.common_info import CommonInfo  # noqa: F401,E501

# NOTE: This file is auto generated by the swagger code generator program.
# Do not edit the class manually.


class Device(object):

    swagger_types = {
        'id': 'str',
        'label': 'str',
        'type': 'str',
        'version': 'str',
        'name': 'str',
        'key': 'str',
        'errors': 'list[str]',
        'info': 'CommonInfo',
        'interval': 'int',
        'last_seen': 'datetime',
        'disabled': 'bool'
    }

    attribute_map = {
        'id': '_id',
        'label': 'label',
        'type': 'type',
        'version': 'version',
        'name': 'name',
        'key': 'key',
        'errors': 'errors',
        'info': 'info',
        'interval': 'interval',
        'last_seen': 'last_seen',
        'disabled': 'disabled'
    }

    rattribute_map = {
        '_id': 'id',
        'label': 'label',
        'type': 'type',
        'version': 'version',
        'name': 'name',
        'key': 'key',
        'errors': 'errors',
        'info': 'info',
        'interval': 'interval',
        'last_seen': 'last_seen',
        'disabled': 'disabled'
    }

    def __init__(self, id=None, label=None, type=None, version=None, name=None, key=None, errors=None, info=None, interval=None, last_seen=None, disabled=None):  # noqa: E501
        """Device - a model defined in Swagger"""
        super(Device, self).__init__()

        self._id = None
        self._label = None
        self._type = None
        self._version = None
        self._name = None
        self._key = None
        self._errors = None
        self._info = None
        self._interval = None
        self._last_seen = None
        self._disabled = None
        self.discriminator = None
        self.alt_discriminator = None

        if id is not None:
            self.id = id
        if label is not None:
            self.label = label
        if type is not None:
            self.type = type
        if version is not None:
            self.version = version
        if name is not None:
            self.name = name
        if key is not None:
            self.key = key
        if errors is not None:
            self.errors = errors
        if info is not None:
            self.info = info
        if interval is not None:
            self.interval = interval
        if last_seen is not None:
            self.last_seen = last_seen
        if disabled is not None:
            self.disabled = disabled

    @property
    def id(self):
        """Gets the id of this Device.

        Unique database ID

        :return: The id of this Device.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Device.

        Unique database ID

        :param id: The id of this Device.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def label(self):
        """Gets the label of this Device.


        :return: The label of this Device.
        :rtype: str
        """
        return self._label

    @label.setter
    def label(self, label):
        """Sets the label of this Device.


        :param label: The label of this Device.  # noqa: E501
        :type: str
        """

        self._label = label

    @property
    def type(self):
        """Gets the type of this Device.


        :return: The type of this Device.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this Device.


        :param type: The type of this Device.  # noqa: E501
        :type: str
        """

        self._type = type

    @property
    def version(self):
        """Gets the version of this Device.


        :return: The version of this Device.
        :rtype: str
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this Device.


        :param version: The version of this Device.  # noqa: E501
        :type: str
        """

        self._version = version

    @property
    def name(self):
        """Gets the name of this Device.


        :return: The name of this Device.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this Device.


        :param name: The name of this Device.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def key(self):
        """Gets the key of this Device.


        :return: The key of this Device.
        :rtype: str
        """
        return self._key

    @key.setter
    def key(self, key):
        """Sets the key of this Device.


        :param key: The key of this Device.  # noqa: E501
        :type: str
        """

        self._key = key

    @property
    def errors(self):
        """Gets the errors of this Device.


        :return: The errors of this Device.
        :rtype: list[str]
        """
        return self._errors

    @errors.setter
    def errors(self, errors):
        """Sets the errors of this Device.


        :param errors: The errors of this Device.  # noqa: E501
        :type: list[str]
        """

        self._errors = errors

    @property
    def info(self):
        """Gets the info of this Device.


        :return: The info of this Device.
        :rtype: CommonInfo
        """
        return self._info

    @info.setter
    def info(self, info):
        """Sets the info of this Device.


        :param info: The info of this Device.  # noqa: E501
        :type: CommonInfo
        """

        self._info = info

    @property
    def interval(self):
        """Gets the interval of this Device.


        :return: The interval of this Device.
        :rtype: int
        """
        return self._interval

    @interval.setter
    def interval(self, interval):
        """Sets the interval of this Device.


        :param interval: The interval of this Device.  # noqa: E501
        :type: int
        """

        self._interval = interval

    @property
    def last_seen(self):
        """Gets the last_seen of this Device.


        :return: The last_seen of this Device.
        :rtype: datetime
        """
        return self._last_seen

    @last_seen.setter
    def last_seen(self, last_seen):
        """Sets the last_seen of this Device.


        :param last_seen: The last_seen of this Device.  # noqa: E501
        :type: datetime
        """

        self._last_seen = last_seen

    @property
    def disabled(self):
        """Gets the disabled of this Device.


        :return: The disabled of this Device.
        :rtype: bool
        """
        return self._disabled

    @disabled.setter
    def disabled(self, disabled):
        """Sets the disabled of this Device.


        :param disabled: The disabled of this Device.  # noqa: E501
        :type: bool
        """

        self._disabled = disabled


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
        if not isinstance(other, Device):
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

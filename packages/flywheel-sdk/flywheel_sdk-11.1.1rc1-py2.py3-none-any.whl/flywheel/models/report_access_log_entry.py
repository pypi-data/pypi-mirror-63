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

from flywheel.models.report_access_log_context import ReportAccessLogContext  # noqa: F401,E501
from flywheel.models.report_access_log_origin import ReportAccessLogOrigin  # noqa: F401,E501

# NOTE: This file is auto generated by the swagger code generator program.
# Do not edit the class manually.


class ReportAccessLogEntry(object):

    swagger_types = {
        'id': 'str',
        'access_type': 'str',
        'context': 'ReportAccessLogContext',
        'origin': 'ReportAccessLogOrigin',
        'request_method': 'str',
        'request_path': 'str',
        'timestamp': 'datetime'
    }

    attribute_map = {
        'id': '_id',
        'access_type': 'access_type',
        'context': 'context',
        'origin': 'origin',
        'request_method': 'request_method',
        'request_path': 'request_path',
        'timestamp': 'timestamp'
    }

    rattribute_map = {
        '_id': 'id',
        'access_type': 'access_type',
        'context': 'context',
        'origin': 'origin',
        'request_method': 'request_method',
        'request_path': 'request_path',
        'timestamp': 'timestamp'
    }

    def __init__(self, id=None, access_type=None, context=None, origin=None, request_method=None, request_path=None, timestamp=None):  # noqa: E501
        """ReportAccessLogEntry - a model defined in Swagger"""
        super(ReportAccessLogEntry, self).__init__()

        self._id = None
        self._access_type = None
        self._context = None
        self._origin = None
        self._request_method = None
        self._request_path = None
        self._timestamp = None
        self.discriminator = None
        self.alt_discriminator = None

        if id is not None:
            self.id = id
        if access_type is not None:
            self.access_type = access_type
        if context is not None:
            self.context = context
        if origin is not None:
            self.origin = origin
        if request_method is not None:
            self.request_method = request_method
        if request_path is not None:
            self.request_path = request_path
        if timestamp is not None:
            self.timestamp = timestamp

    @property
    def id(self):
        """Gets the id of this ReportAccessLogEntry.

        The access log entry id

        :return: The id of this ReportAccessLogEntry.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this ReportAccessLogEntry.

        The access log entry id

        :param id: The id of this ReportAccessLogEntry.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def access_type(self):
        """Gets the access_type of this ReportAccessLogEntry.

        A named field used in the access log report

        :return: The access_type of this ReportAccessLogEntry.
        :rtype: str
        """
        return self._access_type

    @access_type.setter
    def access_type(self, access_type):
        """Sets the access_type of this ReportAccessLogEntry.

        A named field used in the access log report

        :param access_type: The access_type of this ReportAccessLogEntry.  # noqa: E501
        :type: str
        """

        self._access_type = access_type

    @property
    def context(self):
        """Gets the context of this ReportAccessLogEntry.


        :return: The context of this ReportAccessLogEntry.
        :rtype: ReportAccessLogContext
        """
        return self._context

    @context.setter
    def context(self, context):
        """Sets the context of this ReportAccessLogEntry.


        :param context: The context of this ReportAccessLogEntry.  # noqa: E501
        :type: ReportAccessLogContext
        """

        self._context = context

    @property
    def origin(self):
        """Gets the origin of this ReportAccessLogEntry.


        :return: The origin of this ReportAccessLogEntry.
        :rtype: ReportAccessLogOrigin
        """
        return self._origin

    @origin.setter
    def origin(self, origin):
        """Sets the origin of this ReportAccessLogEntry.


        :param origin: The origin of this ReportAccessLogEntry.  # noqa: E501
        :type: ReportAccessLogOrigin
        """

        self._origin = origin

    @property
    def request_method(self):
        """Gets the request_method of this ReportAccessLogEntry.

        The http request method (e.g. GET, PUT, POST, DELETE)

        :return: The request_method of this ReportAccessLogEntry.
        :rtype: str
        """
        return self._request_method

    @request_method.setter
    def request_method(self, request_method):
        """Sets the request_method of this ReportAccessLogEntry.

        The http request method (e.g. GET, PUT, POST, DELETE)

        :param request_method: The request_method of this ReportAccessLogEntry.  # noqa: E501
        :type: str
        """

        self._request_method = request_method

    @property
    def request_path(self):
        """Gets the request_path of this ReportAccessLogEntry.

        The HTTP request path (e.g. /api/projects)

        :return: The request_path of this ReportAccessLogEntry.
        :rtype: str
        """
        return self._request_path

    @request_path.setter
    def request_path(self, request_path):
        """Sets the request_path of this ReportAccessLogEntry.

        The HTTP request path (e.g. /api/projects)

        :param request_path: The request_path of this ReportAccessLogEntry.  # noqa: E501
        :type: str
        """

        self._request_path = request_path

    @property
    def timestamp(self):
        """Gets the timestamp of this ReportAccessLogEntry.


        :return: The timestamp of this ReportAccessLogEntry.
        :rtype: datetime
        """
        return self._timestamp

    @timestamp.setter
    def timestamp(self, timestamp):
        """Sets the timestamp of this ReportAccessLogEntry.


        :param timestamp: The timestamp of this ReportAccessLogEntry.  # noqa: E501
        :type: datetime
        """

        self._timestamp = timestamp


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
        if not isinstance(other, ReportAccessLogEntry):
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

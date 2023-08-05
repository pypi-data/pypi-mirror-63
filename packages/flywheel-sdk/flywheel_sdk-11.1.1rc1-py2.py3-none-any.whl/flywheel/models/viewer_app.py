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


class ViewerApp(object):

    swagger_types = {
        'name': 'str',
        'url': 'str',
        'options': 'object',
        'files': 'dict(str, dict(str, str))',
        'containers': 'dict(str, dict(str, str))'
    }

    attribute_map = {
        'name': 'name',
        'url': 'url',
        'options': 'options',
        'files': 'files',
        'containers': 'containers'
    }

    rattribute_map = {
        'name': 'name',
        'url': 'url',
        'options': 'options',
        'files': 'files',
        'containers': 'containers'
    }

    def __init__(self, name=None, url=None, options=None, files=None, containers=None):  # noqa: E501
        """ViewerApp - a model defined in Swagger"""
        super(ViewerApp, self).__init__()

        self._name = None
        self._url = None
        self._options = None
        self._files = None
        self._containers = None
        self.discriminator = None
        self.alt_discriminator = None

        self.name = name
        self.url = url
        if options is not None:
            self.options = options
        if files is not None:
            self.files = files
        if containers is not None:
            self.containers = containers

    @property
    def name(self):
        """Gets the name of this ViewerApp.

        Unique name of this application

        :return: The name of this ViewerApp.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this ViewerApp.

        Unique name of this application

        :param name: The name of this ViewerApp.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def url(self):
        """Gets the url of this ViewerApp.

        URL that points to the location where the application is hosted

        :return: The url of this ViewerApp.
        :rtype: str
        """
        return self._url

    @url.setter
    def url(self, url):
        """Sets the url of this ViewerApp.

        URL that points to the location where the application is hosted

        :param url: The url of this ViewerApp.  # noqa: E501
        :type: str
        """

        self._url = url

    @property
    def options(self):
        """Gets the options of this ViewerApp.

        General properties passed to the application when it connects to Flywheel

        :return: The options of this ViewerApp.
        :rtype: object
        """
        return self._options

    @options.setter
    def options(self, options):
        """Sets the options of this ViewerApp.

        General properties passed to the application when it connects to Flywheel

        :param options: The options of this ViewerApp.  # noqa: E501
        :type: object
        """

        self._options = options

    @property
    def files(self):
        """Gets the files of this ViewerApp.

        File types that are associated to this application

        :return: The files of this ViewerApp.
        :rtype: dict(str, dict(str, str))
        """
        return self._files

    @files.setter
    def files(self, files):
        """Sets the files of this ViewerApp.

        File types that are associated to this application

        :param files: The files of this ViewerApp.  # noqa: E501
        :type: dict(str, dict(str, str))
        """

        self._files = files

    @property
    def containers(self):
        """Gets the containers of this ViewerApp.

        Container types that are associated to this application

        :return: The containers of this ViewerApp.
        :rtype: dict(str, dict(str, str))
        """
        return self._containers

    @containers.setter
    def containers(self, containers):
        """Sets the containers of this ViewerApp.

        Container types that are associated to this application

        :param containers: The containers of this ViewerApp.  # noqa: E501
        :type: dict(str, dict(str, str))
        """

        self._containers = containers


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
        if not isinstance(other, ViewerApp):
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

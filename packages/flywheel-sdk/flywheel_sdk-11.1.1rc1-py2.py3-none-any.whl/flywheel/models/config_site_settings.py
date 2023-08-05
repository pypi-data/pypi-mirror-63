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

from flywheel.models.provider_links import ProviderLinks  # noqa: F401,E501
from flywheel.models.viewer_app import ViewerApp  # noqa: F401,E501

# NOTE: This file is auto generated by the swagger code generator program.
# Do not edit the class manually.


class ConfigSiteSettings(object):

    swagger_types = {
        'created': 'str',
        'modified': 'str',
        'center_gears': 'list[str]',
        'providers': 'ProviderLinks',
        'viewer_apps': 'list[ViewerApp]'
    }

    attribute_map = {
        'created': 'created',
        'modified': 'modified',
        'center_gears': 'center_gears',
        'providers': 'providers',
        'viewer_apps': 'viewer_apps'
    }

    rattribute_map = {
        'created': 'created',
        'modified': 'modified',
        'center_gears': 'center_gears',
        'providers': 'providers',
        'viewer_apps': 'viewer_apps'
    }

    def __init__(self, created=None, modified=None, center_gears=None, providers=None, viewer_apps=None):  # noqa: E501
        """ConfigSiteSettings - a model defined in Swagger"""
        super(ConfigSiteSettings, self).__init__()

        self._created = None
        self._modified = None
        self._center_gears = None
        self._providers = None
        self._viewer_apps = None
        self.discriminator = None
        self.alt_discriminator = None

        self.created = created
        self.modified = modified
        self.center_gears = center_gears
        if providers is not None:
            self.providers = providers
        if viewer_apps is not None:
            self.viewer_apps = viewer_apps

    @property
    def created(self):
        """Gets the created of this ConfigSiteSettings.


        :return: The created of this ConfigSiteSettings.
        :rtype: str
        """
        return self._created

    @created.setter
    def created(self, created):
        """Sets the created of this ConfigSiteSettings.


        :param created: The created of this ConfigSiteSettings.  # noqa: E501
        :type: str
        """

        self._created = created

    @property
    def modified(self):
        """Gets the modified of this ConfigSiteSettings.


        :return: The modified of this ConfigSiteSettings.
        :rtype: str
        """
        return self._modified

    @modified.setter
    def modified(self, modified):
        """Sets the modified of this ConfigSiteSettings.


        :param modified: The modified of this ConfigSiteSettings.  # noqa: E501
        :type: str
        """

        self._modified = modified

    @property
    def center_gears(self):
        """Gets the center_gears of this ConfigSiteSettings.

        A list of gear algorithm names that are treated as center-pays for the purpose of the billing report

        :return: The center_gears of this ConfigSiteSettings.
        :rtype: list[str]
        """
        return self._center_gears

    @center_gears.setter
    def center_gears(self, center_gears):
        """Sets the center_gears of this ConfigSiteSettings.

        A list of gear algorithm names that are treated as center-pays for the purpose of the billing report

        :param center_gears: The center_gears of this ConfigSiteSettings.  # noqa: E501
        :type: list[str]
        """

        self._center_gears = center_gears

    @property
    def providers(self):
        """Gets the providers of this ConfigSiteSettings.


        :return: The providers of this ConfigSiteSettings.
        :rtype: ProviderLinks
        """
        return self._providers

    @providers.setter
    def providers(self, providers):
        """Sets the providers of this ConfigSiteSettings.


        :param providers: The providers of this ConfigSiteSettings.  # noqa: E501
        :type: ProviderLinks
        """

        self._providers = providers

    @property
    def viewer_apps(self):
        """Gets the viewer_apps of this ConfigSiteSettings.

        A list of viewer app associations for files and container

        :return: The viewer_apps of this ConfigSiteSettings.
        :rtype: list[ViewerApp]
        """
        return self._viewer_apps

    @viewer_apps.setter
    def viewer_apps(self, viewer_apps):
        """Sets the viewer_apps of this ConfigSiteSettings.

        A list of viewer app associations for files and container

        :param viewer_apps: The viewer_apps of this ConfigSiteSettings.  # noqa: E501
        :type: list[ViewerApp]
        """

        self._viewer_apps = viewer_apps


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
        if not isinstance(other, ConfigSiteSettings):
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

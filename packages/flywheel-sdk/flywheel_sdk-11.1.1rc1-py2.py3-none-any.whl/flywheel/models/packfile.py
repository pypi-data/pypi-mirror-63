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

from flywheel.models.packfile_acquisition_input import PackfileAcquisitionInput  # noqa: F401,E501
from flywheel.models.packfile_packfile_input import PackfilePackfileInput  # noqa: F401,E501
from flywheel.models.packfile_project_input import PackfileProjectInput  # noqa: F401,E501
from flywheel.models.packfile_session_input import PackfileSessionInput  # noqa: F401,E501

# NOTE: This file is auto generated by the swagger code generator program.
# Do not edit the class manually.


class Packfile(object):

    swagger_types = {
        'project': 'PackfileProjectInput',
        'session': 'PackfileSessionInput',
        'acquisition': 'PackfileAcquisitionInput',
        'packfile': 'PackfilePackfileInput'
    }

    attribute_map = {
        'project': 'project',
        'session': 'session',
        'acquisition': 'acquisition',
        'packfile': 'packfile'
    }

    rattribute_map = {
        'project': 'project',
        'session': 'session',
        'acquisition': 'acquisition',
        'packfile': 'packfile'
    }

    def __init__(self, project=None, session=None, acquisition=None, packfile=None):  # noqa: E501
        """Packfile - a model defined in Swagger"""
        super(Packfile, self).__init__()

        self._project = None
        self._session = None
        self._acquisition = None
        self._packfile = None
        self.discriminator = None
        self.alt_discriminator = None

        if project is not None:
            self.project = project
        if session is not None:
            self.session = session
        if acquisition is not None:
            self.acquisition = acquisition
        if packfile is not None:
            self.packfile = packfile

    @property
    def project(self):
        """Gets the project of this Packfile.


        :return: The project of this Packfile.
        :rtype: PackfileProjectInput
        """
        return self._project

    @project.setter
    def project(self, project):
        """Sets the project of this Packfile.


        :param project: The project of this Packfile.  # noqa: E501
        :type: PackfileProjectInput
        """

        self._project = project

    @property
    def session(self):
        """Gets the session of this Packfile.


        :return: The session of this Packfile.
        :rtype: PackfileSessionInput
        """
        return self._session

    @session.setter
    def session(self, session):
        """Sets the session of this Packfile.


        :param session: The session of this Packfile.  # noqa: E501
        :type: PackfileSessionInput
        """

        self._session = session

    @property
    def acquisition(self):
        """Gets the acquisition of this Packfile.


        :return: The acquisition of this Packfile.
        :rtype: PackfileAcquisitionInput
        """
        return self._acquisition

    @acquisition.setter
    def acquisition(self, acquisition):
        """Sets the acquisition of this Packfile.


        :param acquisition: The acquisition of this Packfile.  # noqa: E501
        :type: PackfileAcquisitionInput
        """

        self._acquisition = acquisition

    @property
    def packfile(self):
        """Gets the packfile of this Packfile.


        :return: The packfile of this Packfile.
        :rtype: PackfilePackfileInput
        """
        return self._packfile

    @packfile.setter
    def packfile(self, packfile):
        """Sets the packfile of this Packfile.


        :param packfile: The packfile of this Packfile.  # noqa: E501
        :type: PackfilePackfileInput
        """

        self._packfile = packfile


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
        if not isinstance(other, Packfile):
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

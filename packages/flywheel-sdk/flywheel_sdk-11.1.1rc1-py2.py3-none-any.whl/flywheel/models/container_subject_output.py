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

from flywheel.models.analysis_output import AnalysisOutput  # noqa: F401,E501
from flywheel.models.common_info import CommonInfo  # noqa: F401,E501
from flywheel.models.container_output import ContainerOutput  # noqa: F401,E501
from flywheel.models.container_parents import ContainerParents  # noqa: F401,E501
from flywheel.models.file_entry import FileEntry  # noqa: F401,E501
from flywheel.models.note import Note  # noqa: F401,E501
from flywheel.models.permission import Permission  # noqa: F401,E501
from flywheel.models.subject import Subject  # noqa: F401,E501

# NOTE: This file is auto generated by the swagger code generator program.
# Do not edit the class manually.

from .mixins import SubjectMixin

class ContainerSubjectOutput(SubjectMixin):

    swagger_types = {
        'id': 'str',
        'project': 'str',
        'firstname': 'str',
        'lastname': 'str',
        'age': 'int',
        'sex': 'str',
        'cohort': 'str',
        'type': 'str',
        'race': 'str',
        'ethnicity': 'str',
        'species': 'str',
        'strain': 'str',
        'label': 'str',
        'code': 'str',
        'master_code': 'str',
        'tags': 'list[str]',
        'info': 'CommonInfo',
        'files': 'list[FileEntry]',
        'parents': 'ContainerParents',
        'created': 'datetime',
        'modified': 'datetime',
        'revision': 'int',
        'permissions': 'list[Permission]',
        'notes': 'list[Note]',
        'info_exists': 'bool',
        'analyses': 'list[AnalysisOutput]'
    }

    attribute_map = {
        'id': '_id',
        'project': 'project',
        'firstname': 'firstname',
        'lastname': 'lastname',
        'age': 'age',
        'sex': 'sex',
        'cohort': 'cohort',
        'type': 'type',
        'race': 'race',
        'ethnicity': 'ethnicity',
        'species': 'species',
        'strain': 'strain',
        'label': 'label',
        'code': 'code',
        'master_code': 'master_code',
        'tags': 'tags',
        'info': 'info',
        'files': 'files',
        'parents': 'parents',
        'created': 'created',
        'modified': 'modified',
        'revision': 'revision',
        'permissions': 'permissions',
        'notes': 'notes',
        'info_exists': 'info_exists',
        'analyses': 'analyses'
    }

    rattribute_map = {
        '_id': 'id',
        'project': 'project',
        'firstname': 'firstname',
        'lastname': 'lastname',
        'age': 'age',
        'sex': 'sex',
        'cohort': 'cohort',
        'type': 'type',
        'race': 'race',
        'ethnicity': 'ethnicity',
        'species': 'species',
        'strain': 'strain',
        'label': 'label',
        'code': 'code',
        'master_code': 'master_code',
        'tags': 'tags',
        'info': 'info',
        'files': 'files',
        'parents': 'parents',
        'created': 'created',
        'modified': 'modified',
        'revision': 'revision',
        'permissions': 'permissions',
        'notes': 'notes',
        'info_exists': 'info_exists',
        'analyses': 'analyses'
    }

    def __init__(self, id=None, project=None, firstname=None, lastname=None, age=None, sex=None, cohort=None, type=None, race=None, ethnicity=None, species=None, strain=None, label=None, code=None, master_code=None, tags=None, info=None, files=None, parents=None, created=None, modified=None, revision=None, permissions=None, notes=None, info_exists=None, analyses=None):  # noqa: E501
        """ContainerSubjectOutput - a model defined in Swagger"""
        super(ContainerSubjectOutput, self).__init__()

        self._id = None
        self._project = None
        self._firstname = None
        self._lastname = None
        self._age = None
        self._sex = None
        self._cohort = None
        self._type = None
        self._race = None
        self._ethnicity = None
        self._species = None
        self._strain = None
        self._label = None
        self._code = None
        self._master_code = None
        self._tags = None
        self._info = None
        self._files = None
        self._parents = None
        self._created = None
        self._modified = None
        self._revision = None
        self._permissions = None
        self._notes = None
        self._info_exists = None
        self._analyses = None
        self.discriminator = None
        self.alt_discriminator = None

        if id is not None:
            self.id = id
        if project is not None:
            self.project = project
        if firstname is not None:
            self.firstname = firstname
        if lastname is not None:
            self.lastname = lastname
        if age is not None:
            self.age = age
        if sex is not None:
            self.sex = sex
        if cohort is not None:
            self.cohort = cohort
        if type is not None:
            self.type = type
        if race is not None:
            self.race = race
        if ethnicity is not None:
            self.ethnicity = ethnicity
        if species is not None:
            self.species = species
        if strain is not None:
            self.strain = strain
        if label is not None:
            self.label = label
        if code is not None:
            self.code = code
        if master_code is not None:
            self.master_code = master_code
        if tags is not None:
            self.tags = tags
        if info is not None:
            self.info = info
        if files is not None:
            self.files = files
        if parents is not None:
            self.parents = parents
        if created is not None:
            self.created = created
        if modified is not None:
            self.modified = modified
        if revision is not None:
            self.revision = revision
        if permissions is not None:
            self.permissions = permissions
        if notes is not None:
            self.notes = notes
        if info_exists is not None:
            self.info_exists = info_exists
        if analyses is not None:
            self.analyses = analyses

    @property
    def id(self):
        """Gets the id of this ContainerSubjectOutput.

        Unique database ID

        :return: The id of this ContainerSubjectOutput.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this ContainerSubjectOutput.

        Unique database ID

        :param id: The id of this ContainerSubjectOutput.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def project(self):
        """Gets the project of this ContainerSubjectOutput.

        Unique database ID

        :return: The project of this ContainerSubjectOutput.
        :rtype: str
        """
        return self._project

    @project.setter
    def project(self, project):
        """Sets the project of this ContainerSubjectOutput.

        Unique database ID

        :param project: The project of this ContainerSubjectOutput.  # noqa: E501
        :type: str
        """

        self._project = project

    @property
    def firstname(self):
        """Gets the firstname of this ContainerSubjectOutput.

        First name

        :return: The firstname of this ContainerSubjectOutput.
        :rtype: str
        """
        return self._firstname

    @firstname.setter
    def firstname(self, firstname):
        """Sets the firstname of this ContainerSubjectOutput.

        First name

        :param firstname: The firstname of this ContainerSubjectOutput.  # noqa: E501
        :type: str
        """

        self._firstname = firstname

    @property
    def lastname(self):
        """Gets the lastname of this ContainerSubjectOutput.

        Last name

        :return: The lastname of this ContainerSubjectOutput.
        :rtype: str
        """
        return self._lastname

    @lastname.setter
    def lastname(self, lastname):
        """Sets the lastname of this ContainerSubjectOutput.

        Last name

        :param lastname: The lastname of this ContainerSubjectOutput.  # noqa: E501
        :type: str
        """

        self._lastname = lastname

    @property
    def age(self):
        """Gets the age of this ContainerSubjectOutput.

        Age at time of session, in seconds

        :return: The age of this ContainerSubjectOutput.
        :rtype: int
        """
        return self._age

    @age.setter
    def age(self, age):
        """Sets the age of this ContainerSubjectOutput.

        Age at time of session, in seconds

        :param age: The age of this ContainerSubjectOutput.  # noqa: E501
        :type: int
        """

        self._age = age

    @property
    def sex(self):
        """Gets the sex of this ContainerSubjectOutput.


        :return: The sex of this ContainerSubjectOutput.
        :rtype: str
        """
        return self._sex

    @sex.setter
    def sex(self, sex):
        """Sets the sex of this ContainerSubjectOutput.


        :param sex: The sex of this ContainerSubjectOutput.  # noqa: E501
        :type: str
        """

        self._sex = sex

    @property
    def cohort(self):
        """Gets the cohort of this ContainerSubjectOutput.


        :return: The cohort of this ContainerSubjectOutput.
        :rtype: str
        """
        return self._cohort

    @cohort.setter
    def cohort(self, cohort):
        """Sets the cohort of this ContainerSubjectOutput.


        :param cohort: The cohort of this ContainerSubjectOutput.  # noqa: E501
        :type: str
        """

        self._cohort = cohort

    @property
    def type(self):
        """Gets the type of this ContainerSubjectOutput.


        :return: The type of this ContainerSubjectOutput.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this ContainerSubjectOutput.


        :param type: The type of this ContainerSubjectOutput.  # noqa: E501
        :type: str
        """

        self._type = type

    @property
    def race(self):
        """Gets the race of this ContainerSubjectOutput.


        :return: The race of this ContainerSubjectOutput.
        :rtype: str
        """
        return self._race

    @race.setter
    def race(self, race):
        """Sets the race of this ContainerSubjectOutput.


        :param race: The race of this ContainerSubjectOutput.  # noqa: E501
        :type: str
        """

        self._race = race

    @property
    def ethnicity(self):
        """Gets the ethnicity of this ContainerSubjectOutput.


        :return: The ethnicity of this ContainerSubjectOutput.
        :rtype: str
        """
        return self._ethnicity

    @ethnicity.setter
    def ethnicity(self, ethnicity):
        """Sets the ethnicity of this ContainerSubjectOutput.


        :param ethnicity: The ethnicity of this ContainerSubjectOutput.  # noqa: E501
        :type: str
        """

        self._ethnicity = ethnicity

    @property
    def species(self):
        """Gets the species of this ContainerSubjectOutput.


        :return: The species of this ContainerSubjectOutput.
        :rtype: str
        """
        return self._species

    @species.setter
    def species(self, species):
        """Sets the species of this ContainerSubjectOutput.


        :param species: The species of this ContainerSubjectOutput.  # noqa: E501
        :type: str
        """

        self._species = species

    @property
    def strain(self):
        """Gets the strain of this ContainerSubjectOutput.


        :return: The strain of this ContainerSubjectOutput.
        :rtype: str
        """
        return self._strain

    @strain.setter
    def strain(self, strain):
        """Sets the strain of this ContainerSubjectOutput.


        :param strain: The strain of this ContainerSubjectOutput.  # noqa: E501
        :type: str
        """

        self._strain = strain

    @property
    def label(self):
        """Gets the label of this ContainerSubjectOutput.

        A unique identifier for the subject

        :return: The label of this ContainerSubjectOutput.
        :rtype: str
        """
        return self._label

    @label.setter
    def label(self, label):
        """Sets the label of this ContainerSubjectOutput.

        A unique identifier for the subject

        :param label: The label of this ContainerSubjectOutput.  # noqa: E501
        :type: str
        """

        self._label = label

    @property
    def code(self):
        """Gets the code of this ContainerSubjectOutput.

        A unique identifier for the subject

        :return: The code of this ContainerSubjectOutput.
        :rtype: str
        """
        return self._code

    @code.setter
    def code(self, code):
        """Sets the code of this ContainerSubjectOutput.

        A unique identifier for the subject

        :param code: The code of this ContainerSubjectOutput.  # noqa: E501
        :type: str
        """

        self._code = code

    @property
    def master_code(self):
        """Gets the master_code of this ContainerSubjectOutput.

        A unique identifier for the subject

        :return: The master_code of this ContainerSubjectOutput.
        :rtype: str
        """
        return self._master_code

    @master_code.setter
    def master_code(self, master_code):
        """Sets the master_code of this ContainerSubjectOutput.

        A unique identifier for the subject

        :param master_code: The master_code of this ContainerSubjectOutput.  # noqa: E501
        :type: str
        """

        self._master_code = master_code

    @property
    def tags(self):
        """Gets the tags of this ContainerSubjectOutput.

        Array of application-specific tags

        :return: The tags of this ContainerSubjectOutput.
        :rtype: list[str]
        """
        return self._tags

    @tags.setter
    def tags(self, tags):
        """Sets the tags of this ContainerSubjectOutput.

        Array of application-specific tags

        :param tags: The tags of this ContainerSubjectOutput.  # noqa: E501
        :type: list[str]
        """

        self._tags = tags

    @property
    def info(self):
        """Gets the info of this ContainerSubjectOutput.


        :return: The info of this ContainerSubjectOutput.
        :rtype: CommonInfo
        """
        return self._info

    @info.setter
    def info(self, info):
        """Sets the info of this ContainerSubjectOutput.


        :param info: The info of this ContainerSubjectOutput.  # noqa: E501
        :type: CommonInfo
        """

        self._info = info

    @property
    def files(self):
        """Gets the files of this ContainerSubjectOutput.


        :return: The files of this ContainerSubjectOutput.
        :rtype: list[FileEntry]
        """
        return self._files

    @files.setter
    def files(self, files):
        """Sets the files of this ContainerSubjectOutput.


        :param files: The files of this ContainerSubjectOutput.  # noqa: E501
        :type: list[FileEntry]
        """

        self._files = files

    @property
    def parents(self):
        """Gets the parents of this ContainerSubjectOutput.


        :return: The parents of this ContainerSubjectOutput.
        :rtype: ContainerParents
        """
        return self._parents

    @parents.setter
    def parents(self, parents):
        """Sets the parents of this ContainerSubjectOutput.


        :param parents: The parents of this ContainerSubjectOutput.  # noqa: E501
        :type: ContainerParents
        """

        self._parents = parents

    @property
    def created(self):
        """Gets the created of this ContainerSubjectOutput.

        Creation time (automatically set)

        :return: The created of this ContainerSubjectOutput.
        :rtype: datetime
        """
        return self._created

    @created.setter
    def created(self, created):
        """Sets the created of this ContainerSubjectOutput.

        Creation time (automatically set)

        :param created: The created of this ContainerSubjectOutput.  # noqa: E501
        :type: datetime
        """

        self._created = created

    @property
    def modified(self):
        """Gets the modified of this ContainerSubjectOutput.

        Last modification time (automatically updated)

        :return: The modified of this ContainerSubjectOutput.
        :rtype: datetime
        """
        return self._modified

    @modified.setter
    def modified(self, modified):
        """Sets the modified of this ContainerSubjectOutput.

        Last modification time (automatically updated)

        :param modified: The modified of this ContainerSubjectOutput.  # noqa: E501
        :type: datetime
        """

        self._modified = modified

    @property
    def revision(self):
        """Gets the revision of this ContainerSubjectOutput.

        An incremental document revision number

        :return: The revision of this ContainerSubjectOutput.
        :rtype: int
        """
        return self._revision

    @revision.setter
    def revision(self, revision):
        """Sets the revision of this ContainerSubjectOutput.

        An incremental document revision number

        :param revision: The revision of this ContainerSubjectOutput.  # noqa: E501
        :type: int
        """

        self._revision = revision

    @property
    def permissions(self):
        """Gets the permissions of this ContainerSubjectOutput.

        Array of user roles

        :return: The permissions of this ContainerSubjectOutput.
        :rtype: list[Permission]
        """
        return self._permissions

    @permissions.setter
    def permissions(self, permissions):
        """Sets the permissions of this ContainerSubjectOutput.

        Array of user roles

        :param permissions: The permissions of this ContainerSubjectOutput.  # noqa: E501
        :type: list[Permission]
        """

        self._permissions = permissions

    @property
    def notes(self):
        """Gets the notes of this ContainerSubjectOutput.


        :return: The notes of this ContainerSubjectOutput.
        :rtype: list[Note]
        """
        return self._notes

    @notes.setter
    def notes(self, notes):
        """Sets the notes of this ContainerSubjectOutput.


        :param notes: The notes of this ContainerSubjectOutput.  # noqa: E501
        :type: list[Note]
        """

        self._notes = notes

    @property
    def info_exists(self):
        """Gets the info_exists of this ContainerSubjectOutput.

        Flag that indicates whether or not info exists on this container

        :return: The info_exists of this ContainerSubjectOutput.
        :rtype: bool
        """
        return self._info_exists

    @info_exists.setter
    def info_exists(self, info_exists):
        """Sets the info_exists of this ContainerSubjectOutput.

        Flag that indicates whether or not info exists on this container

        :param info_exists: The info_exists of this ContainerSubjectOutput.  # noqa: E501
        :type: bool
        """

        self._info_exists = info_exists

    @property
    def analyses(self):
        """Gets the analyses of this ContainerSubjectOutput.


        :return: The analyses of this ContainerSubjectOutput.
        :rtype: list[AnalysisOutput]
        """
        return self._analyses

    @analyses.setter
    def analyses(self, analyses):
        """Sets the analyses of this ContainerSubjectOutput.


        :param analyses: The analyses of this ContainerSubjectOutput.  # noqa: E501
        :type: list[AnalysisOutput]
        """

        self._analyses = analyses


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
        if not isinstance(other, ContainerSubjectOutput):
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

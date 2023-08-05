# coding: utf-8

"""
    Stitch Connect

    https://www.stitchdata.com/docs/developers/stitch-connect/api  # noqa: E501

    The version of the OpenAPI document: 0.1
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from stitch_connect_client.configuration import Configuration


class StreamSchema(object):
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
        'schema': 'str',
        'metadata': 'list[Metadata]',
        'non_discoverable_metadata_keys': 'list[str]'
    }

    attribute_map = {
        'schema': 'schema',
        'metadata': 'metadata',
        'non_discoverable_metadata_keys': 'non-discoverable-metadata-keys'
    }

    def __init__(self, schema=None, metadata=None, non_discoverable_metadata_keys=None, local_vars_configuration=None):  # noqa: E501
        """StreamSchema - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._schema = None
        self._metadata = None
        self._non_discoverable_metadata_keys = None
        self.discriminator = None

        if schema is not None:
            self.schema = schema
        if metadata is not None:
            self.metadata = metadata
        if non_discoverable_metadata_keys is not None:
            self.non_discoverable_metadata_keys = non_discoverable_metadata_keys

    @property
    def schema(self):
        """Gets the schema of this StreamSchema.  # noqa: E501

        The JSON schema describing the stream’s fields.  # noqa: E501

        :return: The schema of this StreamSchema.  # noqa: E501
        :rtype: str
        """
        return self._schema

    @schema.setter
    def schema(self, schema):
        """Sets the schema of this StreamSchema.

        The JSON schema describing the stream’s fields.  # noqa: E501

        :param schema: The schema of this StreamSchema.  # noqa: E501
        :type: str
        """

        self._schema = schema

    @property
    def metadata(self):
        """Gets the metadata of this StreamSchema.  # noqa: E501

        An array of Metadata objects.  # noqa: E501

        :return: The metadata of this StreamSchema.  # noqa: E501
        :rtype: list[Metadata]
        """
        return self._metadata

    @metadata.setter
    def metadata(self, metadata):
        """Sets the metadata of this StreamSchema.

        An array of Metadata objects.  # noqa: E501

        :param metadata: The metadata of this StreamSchema.  # noqa: E501
        :type: list[Metadata]
        """

        self._metadata = metadata

    @property
    def non_discoverable_metadata_keys(self):
        """Gets the non_discoverable_metadata_keys of this StreamSchema.  # noqa: E501

        An array of strings corresponding to `metadata` keys that can be modified.   # noqa: E501

        :return: The non_discoverable_metadata_keys of this StreamSchema.  # noqa: E501
        :rtype: list[str]
        """
        return self._non_discoverable_metadata_keys

    @non_discoverable_metadata_keys.setter
    def non_discoverable_metadata_keys(self, non_discoverable_metadata_keys):
        """Sets the non_discoverable_metadata_keys of this StreamSchema.

        An array of strings corresponding to `metadata` keys that can be modified.   # noqa: E501

        :param non_discoverable_metadata_keys: The non_discoverable_metadata_keys of this StreamSchema.  # noqa: E501
        :type: list[str]
        """

        self._non_discoverable_metadata_keys = non_discoverable_metadata_keys

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
        if not isinstance(other, StreamSchema):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, StreamSchema):
            return True

        return self.to_dict() != other.to_dict()

# coding: utf-8

"""
    Pulp 3 API

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    The version of the OpenAPI document: v3
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import pulpcore.client.pulp_rpm
from pulpcore.client.pulp_rpm.models.inline_response2009 import InlineResponse2009  # noqa: E501
from pulpcore.client.pulp_rpm.rest import ApiException

class TestInlineResponse2009(unittest.TestCase):
    """InlineResponse2009 unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test InlineResponse2009
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = pulpcore.client.pulp_rpm.models.inline_response2009.InlineResponse2009()  # noqa: E501
        if include_optional :
            return InlineResponse2009(
                count = 56, 
                next = '0', 
                previous = '0', 
                results = [
                    pulpcore.client.pulp_rpm.models.rpm/repo_metadata_file.rpm.RepoMetadataFile(
                        pulp_href = '0', 
                        pulp_created = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        artifact = '0', 
                        data_type = '0', 
                        checksum_type = '0', 
                        checksum = '0', 
                        sha256 = '0', )
                    ]
            )
        else :
            return InlineResponse2009(
                count = 56,
                results = [
                    pulpcore.client.pulp_rpm.models.rpm/repo_metadata_file.rpm.RepoMetadataFile(
                        pulp_href = '0', 
                        pulp_created = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), 
                        artifact = '0', 
                        data_type = '0', 
                        checksum_type = '0', 
                        checksum = '0', 
                        sha256 = '0', )
                    ],
        )

    def testInlineResponse2009(self):
        """Test InlineResponse2009"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()

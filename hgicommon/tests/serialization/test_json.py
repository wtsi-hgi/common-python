"""
Legalese
--------
Copyright (c) 2016 Genome Research Ltd.

Author: Colin Nolan <cn13@sanger.ac.uk>

This file is part of HGI's common Python library

This program is free software: you can redistribute it and/or modify it
under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation; either version 3 of the License, or (at
your option) any later version.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser
General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
"""
import json
import unittest

from hgicommon.collections import Metadata
from hgicommon.serialization.json import MetadataJSONEncoder


class TestMetadataJSONEncoder(unittest.TestCase):
    """
    Tests for `MetadataJSONEncoder`.
    """
    def setUp(self):
        self.metadata_as_json = {
            "a": 10,
            "b": "test",
            "c": [1, 2, 3],
            "e": 1.5
        }
        self.metadata = Metadata(self.metadata_as_json)

    def test_default_with_unknown(self):
        self.assertRaises(TypeError, MetadataJSONEncoder().default, object())

    def test_default_with_metadata(self):
        encoded = MetadataJSONEncoder().default(self.metadata)
        self.assertDictEqual(encoded, self.metadata_as_json)

    def test_class_with_json_dumps(self):
        encoded_as_string = json.dumps(self.metadata, cls=MetadataJSONEncoder)
        encoded = json.loads(encoded_as_string)
        self.assertDictEqual(encoded, self.metadata_as_json)


if __name__ == "__main__":
    unittest.main()

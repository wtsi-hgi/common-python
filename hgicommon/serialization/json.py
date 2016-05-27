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
from json import JSONEncoder

from hgijson.types import PrimitiveJsonSerializableType

from hgicommon.collections import Metadata


class MetadataJSONEncoder(JSONEncoder):
    """
    JSON encoder for `Metadata` instances.

    Do not use as target_cls in `json.dumps` if the metadata collection being serialised contains values with types that
    cannot be converted to JSON by default. In such cases, this class can be used in `AutomaticJSONEncoderClassBuilder`
    along with encoders that handle other unsupported types or it should be used within another decoder.
    """
    def default(self, to_encode: Metadata) -> PrimitiveJsonSerializableType:
        if not isinstance(to_encode, Metadata):
            JSONEncoder.default(self, to_encode)

        return to_encode._data

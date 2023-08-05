# coding=UTF-8
# ex:ts=4:sw=4:et=on

# Copyright (c) 2013, Mathijs Dumon
# All rights reserved.
# Complete license can be found in the LICENSE file.

import os, struct
from io import SEEK_SET #, SEEK_CUR, SEEK_END

import numpy as np

from pyxrd.generic.io.utils import get_case_insensitive_glob
from pyxrd.generic.utils import u

from ..base_parser import BaseParser
from .namespace import xrd_parsers
from .xrd_parser_mixin import XRDParserMixin


def cap(lower, value, upper, out=None):
    if value < lower or value > upper:
        return out if out is not None else min(max(value, lower), upper)
    else:
        return value

@xrd_parsers.register_parser()
class RDParser(XRDParserMixin, BaseParser):
    """
        Philips Binary V3 & V5 *.RD format parser
    """

    description = "Phillips Binary V3/V5 *.RD"
    extensions = get_case_insensitive_glob("*.RD")
    mimetypes = ["application/octet-stream", ]

    __file_mode__ = "rb"

    @classmethod
    def _parse_header(cls, filename, fp, data_objects=None, close=False):
        f = fp

        try:
            basename = u(os.path.basename(filename))
        except:
            basename = None

        # Adapt XRDFile list
        data_objects = cls._adapt_data_object_list(data_objects, num_samples=1)

        # Go to the start of the file
        f.seek(0, SEEK_SET)

        # Read file format version:
        version = f.read(2).decode()

        if version in ("V3", "V5"):

            # Read diffractometer, target and focus type:
            f.seek(84, SEEK_SET)
            diffractomer_type, target_type, focus_type = struct.unpack("bbb", f.read(3))
            diffractomer_type = {
                0: b"PW1800",
                1: b"PW1710 based system",
                2: b"PW1840",
                3: b"PW3710 based system",
                4: b"Undefined",
                5: b"X'Pert MPD"
            }[cap(0, diffractomer_type, 5, 4)]
            target_type = {
                0: b"Cu",
                1: b"Mo",
                2: b"Fe",
                3: b"Cr",
                4: b"Other"
            }[cap(0, target_type, 3, 4)]
            focus_type = {
                0: b"BF",
                1: b"NF",
                2: b"FF",
                3: b"LFF",
                4: b"Unkown",
            }[cap(0, focus_type, 3, 4)]

            # Read wavelength information:
            f.seek(94, SEEK_SET)
            alpha1, alpha2, alpha_factor = struct.unpack("ddd", f.read(24))
            # Read sample name:
            f.seek(146, SEEK_SET)
            sample_name = u(f.read(16).replace(b"\0", b""))

            # Read data limits:
            f.seek(214)
            twotheta_step, twotheta_min, twotheta_max = struct.unpack("ddd", f.read(24))
            twotheta_count = int((twotheta_max - twotheta_min) / twotheta_step)

            # Set data start:
            data_start = {
                "V3": 250,
                "V5": 810
            }[version]

            data_objects[0].update(
                filename=basename,
                name=sample_name,
                twotheta_min=twotheta_min,
                twotheta_max=twotheta_max,
                twotheta_step=twotheta_step,
                twotheta_count=twotheta_count,
                target_type=target_type,
                alpha1=alpha1,
                alpha2=alpha2,
                alpha_factor=alpha_factor,
                data_start=data_start,
                version=version
            )

        else:
            raise IOError("Only V3 and V5 *.RD files are supported!")

        if close: f.close()
        return data_objects

    @classmethod
    def _parse_data(cls, filename, fp, data_objects=None, close=False):
        f = fp

        # RD files are singletons, so no need to iterate over the list,
        # there is only one XRDFile instance:
        if data_objects[0].data == None:
            data_objects[0].data = []

        # Parse data:
        if f is not None:
            if data_objects[0].version in ("V3", "V5"):
                # Move to start of data:
                f.seek(data_objects[0].data_start)
                n = 0
                while n < data_objects[0].twotheta_count:
                    y, = struct.unpack("H", f.read(2))
                    data_objects[0].data.append([
                        data_objects[0].twotheta_min + data_objects[0].twotheta_step * float(n + 0.5),
                        float(y)
                    ])
                    n += 1
            else:
                raise IOError("Only V3 and V5 *.RD files are supported!")

        data_objects[0].data = np.array(data_objects[0].data)

        if close: f.close()
        return data_objects

    pass # end of class

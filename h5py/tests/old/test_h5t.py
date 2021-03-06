# This file is part of h5py, a Python interface to the HDF5 library.
#
# http://www.h5py.org
#
# Copyright 2008-2013 Andrew Collette and contributors
#
# License:  Standard 3-clause BSD; see "license.txt" for full license terms
#           and contributor agreement.

from __future__ import absolute_import

try:
    import unittest2 as ut
except ImportError:
    import unittest as ut

from six import text_type

import numpy as np
import h5py
from h5py import h5t

class TestCompound(ut.TestCase):

    """
        Feature: Compound types can be created from Python dtypes
    """

    def test_ref(self):
        """ Reference types are correctly stored in compound types (issue 144)
        """
        ref = h5py.special_dtype(ref=h5py.Reference)
        dt = np.dtype([('a',ref),('b','<f4')])
        tid = h5t.py_create(dt,logical=True)
        t1, t2 = tid.get_member_type(0), tid.get_member_type(1)
        self.assertEqual(t1, h5t.STD_REF_OBJ)
        self.assertEqual(t2, h5t.IEEE_F32LE)
        self.assertEqual(tid.get_member_offset(0), 0)
        self.assertEqual(tid.get_member_offset(1), h5t.STD_REF_OBJ.get_size())

    def test_out_of_order_offsets(self):
        size = 20
        type_dict = {
            'names' : ['f1', 'f2', 'f3'],
            'formats' : ['<f4', '<i4', '<f8'],
            'offsets' : [0, 16, 8]
        }

        expected_dtype = np.dtype(type_dict)

        tid = h5t.create(h5t.COMPOUND, size)
        for name, offset, dt in zip(
                type_dict["names"], type_dict["offsets"], type_dict["formats"]
        ):
            tid.insert(
                name.encode("utf8") if isinstance(name, text_type) else name,
                offset,
                h5t.py_create(dt)
            )

        self.assertEqual(tid.dtype, expected_dtype)
        self.assertEqual(tid.dtype.itemsize, size)

"""Test cases for the Plane class in conversion.py"""
import os
import sys

import unittest
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from conversion import Plane # pylint: disable=wrong-import-position

class TestPlane(unittest.TestCase):
    """Test Case for Plane class"""
    def test_project_on_plane(self):
        """ Test the projection of a vector onto a plane """
        # Create a plane with a normal vector
        plane = Plane(np.array([1, 1, 1]))

        # Test case 1: Zero vector
        vector4 = np.array([0, 0, 0])
        expected4 = np.array([0, 0, 0])
        assert np.allclose(plane.project_on_plane(vector4), expected4)

        print("All test cases passed!")

if __name__ == '__main__':
    unittest.main()

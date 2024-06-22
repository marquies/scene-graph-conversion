"""Test cases for the Plane class in conversion.py"""

import unittest
import numpy as np

from conversion import Plane

class TestPlane(unittest.TestCase):
    """Test Case for Plane class"""
    def test_project_on_plane(self):
        """ Test the projection of a vector onto a plane """
        # Create a plane with a normal vector
        plane = Plane(np.array([1, 1, 1]))

        # Test case 1: Vector perpendicular to the plane
        vector1 = np.array([2, 2, 2])
        expected1 = np.array([0, 0, 0])
        assert np.allclose(plane.project_on_plane(vector1), expected1)

        # Test case 2: Vector parallel to the plane
        vector2 = np.array([1, 1, 1])
        expected2 = np.array([1, 1, 1])
        assert np.allclose(plane.project_on_plane(vector2), expected2)

        # Test case 3: Vector not perpendicular or parallel to the plane
        vector3 = np.array([3, 2, 1])
        expected3 = np.array([1, 0, -1])
        assert np.allclose(plane.project_on_plane(vector3), expected3)

        # Test case 4: Zero vector
        vector4 = np.array([0, 0, 0])
        expected4 = np.array([0, 0, 0])
        assert np.allclose(plane.project_on_plane(vector4), expected4)

        print("All test cases passed!")

if __name__ == '__main__':
    unittest.main()

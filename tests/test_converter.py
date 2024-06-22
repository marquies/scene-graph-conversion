import unittest
from unittest.mock import patch
import numpy as np
from conversion import filter_log_file, Camera

class TestConversion(unittest.TestCase):
    @patch('builtins.open')
    def test_filter_log_file(self, mock_open):
        # Mock the file content
        mock_file_content = [
            '---',
            '0 {"name": "Camera1", "c_00": 1, "c_01": 0, "c_02": 0, "c_03": 0, "c_10": 0, "c_11": 1, "c_12": 0, "c_13": 0, "c_20": 0, "c_21": 0, "c_22": 1, "c_23": 0, "c_30": 0, "c_31": 0, "c_32": 0, "c_33": 1, "pm_00": 1, "pm_01": 0, "pm_02": 0, "pm_03": 0, "pm_10": 0, "pm_11": 1, "pm_12": 0, "pm_13": 0, "pm_20": 0, "pm_21": 0, "pm_22": 1, "pm_23": 0, "pm_30": 0, "pm_31": 0, "pm_32": 0, "pm_33": 1, "depth": 0}',
            '1 {"name": "Camera2", "c_00": 1, "c_01": 0, "c_02": 0, "c_03": 0, "c_10": 0, "c_11": 1, "c_12": 0, "c_13": 0, "c_20": 0, "c_21": 0, "c_22": 1, "c_23": 0, "c_30": 0, "c_31": 0, "c_32": 0, "c_33": 1, "pm_00": 1, "pm_01": 0, "pm_02": 0, "pm_03": 0, "pm_10": 0, "pm_11": 1, "pm_12": 0, "pm_13": 0, "pm_20": 0, "pm_21": 0, "pm_22": 1, "pm_23": 0, "pm_30": 0, "pm_31": 0, "pm_32": 0, "pm_33": 1, "depth": 1}',
            '---',
            '0 {"name": "Object1", "depth":0, "t_x": 1, "t_y": 2, "t_z": 3}',
            '1 {"name": "Object2", "depth":0, "t_x": 4, "t_y": 5, "t_z": 6}',
            '2 {"name": "Object3", "depth":0, "t_x": 7, "t_y": 8, "t_z": 9}',
        ]
        mock_open.return_value.__enter__.return_value.readlines.return_value = mock_file_content

        # Call the function with test data
        file_path = '/path/to/log/file.log'
        cameraname = 'Camera1'
        data, camera = filter_log_file(file_path, cameraname)

        # Assert the expected results
        expected_data = [
            {
                'visibility_state': 0,
                'tree_position': '{"name": "Object1", "t_x": 1, "t_y": 2, "t_z": 3}',
                'json_data': {'name': 'Object1', 't_x': 1, 't_y': 2, 't_z': 3}
            },
            {
                'visibility_state': 1,
                'tree_position': '{"name": "Object2", "t_x": 4, "t_y": 5, "t_z": 6}',
                'json_data': {'name': 'Object2', 't_x': 4, 't_y': 5, 't_z': 6}
            },
            {
                'visibility_state': 2,
                'tree_position': '{"name": "Object3", "t_x": 7, "t_y": 8, "t_z": 9}',
                'json_data': {'name': 'Object3', 't_x': 7, 't_y': 8, 't_z': 9}
            }
        ]
        expected_camera = Camera(
            np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]),
            np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
        )
        self.assertEqual(data, expected_data)
        self.assertEqual(camera.position.tolist(), expected_camera.position.tolist())
        self.assertEqual(camera.projection_matrix.tolist(), expected_camera.projection_matrix.tolist())

if __name__ == '__main__':
    unittest.main()
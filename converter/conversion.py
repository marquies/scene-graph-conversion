"""
Conversion functions for the Unity log file.
"""

import json
import dataclasses
import numpy as np


def filter_log_file(file_path, cameraname):
    """
        This function reads the log file and filters the data for the given camera name.
        It returns the filtered data and the camera object.
        The camera object contains the position and the projection matrix of the camera.

    """
    data = []
    camera = None
    with open(file_path, 'r', encoding="utf-8") as file:

        lines = file.readlines()
        for i in range(0, len(lines), 1):
            if lines[i].strip() == '' or lines[i].startswith('---'):
                continue

            visibility_state, tree_position = lines[i].split(' ', 1)
            # take line and get content of the braces in the line with a regex and convert to json
            pos1 = lines[i].find('{')
            pos2 = lines[i].rfind('}')

            json_data = json.loads(lines[i][pos1:pos2+1])

            #if json_data['state'] == "1" and int(json_data['depth']) <= 0:
            if int(json_data['depth']) <= 0:
                data.append({
                    'visibility_state': int(visibility_state),
                    'tree_position': tree_position.strip(),
                    'json_data': json_data
                })

            if json_data['name'].find(cameraname) > -1:
                x = np.array([[json_data['c_00'], json_data['c_01'],
                                json_data['c_02'], json_data['c_03']],
                              [json_data['c_10'], json_data['c_11'],
                                json_data['c_12'], json_data['c_13']],
                              [json_data['c_20'], json_data['c_21'],
                                json_data['c_22'], json_data['c_23']],
                              [json_data['c_30'], json_data['c_31'],
                                json_data['c_32'], json_data['c_33']]])
                y = np.array([[json_data['pm_00'], json_data['pm_01'],
                                json_data['pm_02'], json_data['pm_03']],
                              [json_data['pm_10'], json_data['pm_11'],
                                json_data['pm_12'], json_data['pm_13']],
                              [json_data['pm_20'], json_data['pm_21'],
                                json_data['pm_22'], json_data['pm_23']],
                            [json_data['pm_30'], json_data['pm_31'],
                             json_data['pm_32'], json_data['pm_33']]])
                camera = Camera(x, y)

    return data, camera

@dataclasses.dataclass
class Tuple:
    """
    This class represents a 3D tuple.
    """
    def __init__(self, x, y, z):
        """
        The constructor takes the x, y, z and w coordinates of the tuple.
        """
        self.x = x
        self.y = y
        self.z = z

@dataclasses.dataclass
class Camera:
    """
    This class represents a camera in 3D space.
    """
    def __init__(self, position, projection_matrix):
        """
        The constructor takes the position and the projection matrix of the camera.
        """
        self.position = position
        self.projection_matrix = projection_matrix

@dataclasses.dataclass
class Plane:
    """
    This class represents a plane in 3D space.
    """
    def __init__(self, normal):
        """
        The constructor takes the normal vector of the plane.
        """
        self.normal = normal

    def project_on_plane(self, vector):
        """
        This method projects the given vector onto the plane.
        It returns the projected vector.
        """
        # Implement the projection of the vector onto the plane defined by the plane's normal
        distance = np.dot(vector, self.normal) / np.linalg.norm(self.normal)
        projection = vector - distance * self.normal
        return projection


class Vector3:
    """
    This class represents a 3D vector.

    """
    def __init__(self, x, y, z, name=None):
        """
        The constructor takes the x, y and z coordinates of the vector.
        """
        self.x = x
        self.y = y
        self.z = z
        self.name = name


    def get_x(self):
        """
        Returns x
        """
        return self.x
    def get_y(self):
        """
        Returns y
        """
        return self.y
    def get_z(self):
        """
        Returns z
        """
        return self.z
    def get_name(self):
        """
        Returns x
        """
        return self.name


    def project(self, camera):
        """
        This method projects the vector from world coordinates to camera coordinates.
        It returns the projected vector.
        """
        camera_inverse = np.linalg.inv(camera.position.copy())
        camera_projection = camera.projection_matrix.copy()

        return self.apply_matrix4x4(camera_inverse).apply_matrix4x4(camera_projection)

    def apply_matrix4x4(self, matrix):
        """
        This method applies the given 4x4 matrix to the vector.
        It returns the transformed vector.
        """
        # Create a 4x1 matrix from the vector
        x = self.x
        y = self.y
        z = self.z
        w = 1 / ( matrix[3][0] * x + matrix[3][1] * y + matrix[3][2] * z + matrix[3][3] )

        self.x = ( matrix[ 0 ][0] * x + matrix[0][1] * y + matrix[0][2] * z +  matrix[0][3] ) * w
        self.y = ( matrix[ 1 ][0] * x + matrix[1][1] * y + matrix[1][2] * z +  matrix[1][3] ) * w
        self.z = ( matrix[ 2 ][0] * x + matrix[2][1] * y + matrix[2][2] * z +  matrix[2][3] ) * w

        return self

    def clone(self):
        """
        This method returns a copy of the vector.
        """
        return Vector3(self.x, self.y, self.z, self.name)


def get_objects_from_input(inputs):
    """
    This function returns a list of Vector3 objects from the given input data.
    The input data is a list of dictionaries, where each dictionary contains the data of an object.
    The Vector3 objects contain the position of the objects in world coordinates.
    """
    objects = []
    for i in range(0, len(inputs), 1):
        #if inputs[i]['json_data']['m_Name'] != "Main Camera":
        objects.append(Vector3(float(inputs[i]['json_data']['t_x']),
                               float(inputs[i]['json_data']['t_y']),
                               float(inputs[i]['json_data']['t_z']),
                               inputs[i]['json_data']['path']))
    return objects


def get_camera_direction(camera, target_position):
    """Calculate the world direction vector from the camera to its target.
    
    Args:
        camera_position (np.ndarray): The camera's position in world coordinates.
        target_position (np.ndarray): The target's position in world coordinates.
    
    Returns:
        np.ndarray: The normalized direction vector from the camera to the target.
    """
    #direction = target_position - camera_position
    target_position[0] = camera[2][0]
    target_position[1] = camera[2][1]
    target_position[2] = camera[2][2]

    return np.linalg.norm(target_position) # optional negate?

def compare_positions(obj_a, obj_b):
    """
    This function compares the positions of two objects in camera space and prints the result.
    """
    left_right = "left" if obj_a.x < obj_b.x else "right"
    left_right = left_right if abs(obj_a.x - obj_b.x) > 0.01 else "same level"
    above_below = "beneath" if obj_a.y < obj_b.y else "above"
    above_below = above_below if abs(obj_a.y - obj_b.y) > 0.01 else "same height"
    front_back = "in front of" if obj_a.z < obj_b.z else "behind"
    front_back = front_back if abs(obj_a.z - obj_b.z) > 0.01 else "same depth"

    print(f"\n object {obj_a.name} is {obj_b} of object {obj_b.name}"+
          f" and {above_below} object {obj_b.name} and {front_back} object {obj_b.name}.")
    return [Tuple(obj_a.name, left_right, obj_b.name),
            Tuple(obj_a.name, above_below, obj_b.name), Tuple(obj_a.name, front_back, obj_b.name)]

def determine_arrangement2(camera, objects):
    """
    This function determines the arrangement of the objects in camera space and prints the result.
    """
    tuples = []
    for i in range(len(objects)):
        obj_in_camera_space = objects[i].clone().project(camera)
        for j in range(len(objects)):
            if i != j:
                tpl = compare_positions(obj_in_camera_space, objects[j].clone().project(camera))
                # append tuple array elements to tuples
                for t in tpl:
                    tuples.append(t)
    return tuples

def remove_bidirectional_duplicates(tuples):
    """
    Removes bidirectional duplicates from the list of tuples.
    """
    seen = set()
    result = []
    for item in tuples:
        obj = item.x
        predicate = item.y
        subject = item.z
        if (obj, predicate, subject) not in seen:
            seen.add((subject, predicate, obj))
            result.append(Tuple(subject, predicate, obj))
    return result

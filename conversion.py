import json
import numpy as np
import json
import pyyed


def filter_log_file(file_path, cameraname):
    """
        This function reads the log file and filters the data for the given camera name.
        It returns the filtered data and the camera object.
        The camera object contains the position and the projection matrix of the camera.

    """
    data = []
    camera = None
    with open(file_path, 'r') as file:

        lines = file.readlines()
        for i in range(0, len(lines), 1):
            if lines[i].strip() == '' or lines[i].startswith('---'):
                continue

            visibility_state, tree_position = lines[i].split(' ', 1)
            # take line and get content of the braces in the line with a regex and convert to json
            pos1 = lines[i].find('{')
            pos2 = lines[i].rfind('}')

            json_data = json.loads(lines[i][pos1:pos2+1])

            if json_data['state'] == "1" and int(json_data['depth']) <= 3:
                
                data.append({
                    'visibility_state': int(visibility_state),
                    'tree_position': tree_position.strip(),
                    'json_data': json_data
                })
            
            if json_data['name'].find(cameraname) > -1:
                x = np.array([[json_data['c_00'], json_data['c_01'], json_data['c_02'], json_data['c_03']],
                                   [json_data['c_10'], json_data['c_11'], json_data['c_12'], json_data['c_13']],
                                   [json_data['c_20'], json_data['c_21'], json_data['c_22'], json_data['c_23']],
                                   [json_data['c_30'], json_data['c_31'], json_data['c_32'], json_data['c_33']]])
                y      = np.array([[json_data['pm_00'], json_data['pm_01'], json_data['pm_02'], json_data['pm_03']],
                                   [json_data['pm_10'], json_data['pm_11'], json_data['pm_12'], json_data['pm_13']],
                                   [json_data['pm_20'], json_data['pm_21'], json_data['pm_22'], json_data['pm_23']],
                                   [json_data['pm_30'], json_data['pm_31'], json_data['pm_32'], json_data['pm_33']]])
                camera = Camera(x, y)
            
    return data, camera

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



def transform_vector(matrix, json_str):
    """
    This function transforms the given vector with the given matrix.
    The vector is given as a JSON string and the matrix is given as a 4x4 list of lists.
    The function returns the transformed vector as a JSON string.
    """
    # Parse the JSON string to get the vector values
    data = json.loads(json_str)
    vector = np.array([data['x'], data['y'], data['z'], 1])

    # Perform the matrix transformation
    

    # Return the transformed vector
    return transformed_vector



def getObjectsFromInput(inputs):
    """
    This function returns a list of Vector3 objects from the given input data.
    The input data is a list of dictionaries, where each dictionary contains the data of an object.
    The Vector3 objects contain the position of the objects in world coordinates.
    """
    objects = []
    for i in range(0, len(inputs), 1):
        #if inputs[i]['json_data']['m_Name'] != "Main Camera":
        objects.append(Vector3(float(inputs[i]['json_data']['t_x']), float(inputs[i]['json_data']['t_y']), float(inputs[i]['json_data']['t_z']), inputs[i]['json_data']['path']))
    return objects

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
    
    return np.linalg.norm(target_position) #TODO Negate???

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


    def x(self):
        return self.x
    def y(self):
        return self.y
    def z(self):
        return self.z
    def name(self):
        return self.name
    
        
    def project(self, camera):
        """
        This method projects the vector from world coordinates to camera coordinates.
        It returns the projected vector.
        """
        

        camera_inverse = np.linalg.inv(camera.position.copy())
        camera_projection = camera.projection_matrix.copy()
        
        return self.applyMatrix4x4(camera_inverse).applyMatrix4x4(camera_projection)

    def applyMatrix4x4(self, matrix):
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
    
def compare_positions(objA, objB):
    """
    This function compares the positions of two objects in camera space and prints the result.
    """
    left_right = "links" if objA.x < objB.x else "rechts"
    left_right = left_right if abs(objA.x - objB.x) > 0.01 else "selbe ebene"
    above_below = "unter" if objA.y < objB.y else "über"
    above_below = above_below if abs(objA.y - objB.y) > 0.01 else "selbe höhe"
    front_back = "vor" if objA.z < objB.z else "hinter"
    front_back = front_back if abs(objA.z - objB.z) > 0.01 else "selbe Tiefe"

    print(f"\n Objekt {objA.name} ist {left_right} von Objekt {objB.name} und {above_below} Objekt {objB.name} und {front_back} Objekt {objB.name}.")
    return [Tuple(objA.name, left_right, objB.name), Tuple(objA.name, above_below, objB.name), Tuple(objA.name, front_back, objB.name)]

def determine_arrangement2(camera, objects):
    """
    This function determines the arrangement of the objects in camera space and prints the result.
    """
    tuples = []
    for i in range(len(objects)):
        objInCameraSpace = objects[i].clone().project(camera)
        for j in range(len(objects)):
            if i != j:
                tuple = compare_positions(objInCameraSpace, objects[j].clone().project(camera))
                # appent tuple array elements to tuples
                for t in tuple:
                    tuples.append(t)
    return tuples


inputs, camera = filter_log_file("input_data/scenegraphlog4.log", "Main Camera")

print("Found " + str(len(inputs)) + " objects in the log file.  ")


objects = getObjectsFromInput(inputs)

print("Filtered " + str(len(objects)) + " objects from the log file.   ")

tuples = determine_arrangement2(camera, objects)

g = pyyed.Graph()

for i in range(len(tuples)):
    if (tuples[i].x not in g.nodes):
        g.add_node(tuples[i].x)
    if (tuples[i].z not in g.nodes):
        g.add_node(tuples[i].z)
    g.add_edge(tuples[i].x, tuples[i].z).add_label(tuples[i].y)

print("Added " + str(len(g.nodes)) + " nodes and " + str(len(g.edges)) + " edges to the graph.   ")
#g.add_node('foo', font_family="Zapfino")
#g.add_node('foo2', shape="roundrectangle", font_style="bolditalic", underlined_text="true")

#g.add_edge('foo1', 'foo2')
#g.add_node('abc', font_size="72", height="100")

#g.add_node('bar', label="Multi\nline\ntext")
#g.add_node('foobar', label="""Multi
#Line
#Text!""")
    
#print(g.get_graph())

# To write to file:
with open('test_graph.graphml', 'w') as fp:
    fp.write(g.get_graph())


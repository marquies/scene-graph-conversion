import json
import numpy as np
import json

def filter_log_file(file_path, cameraname):
    data = []
    camera = None
    with open(file_path, 'r') as file:
    #    for line in file:
    #        text, json_str = line.rsplit(' ', 1)
    #        if filter_value in text:
    #            result.append(json.loads(json_str))
        lines = file.readlines()
        for i in range(0, len(lines), 1):
            if lines[i].strip() == '' or lines[i].startswith('---'):
                continue

            visibility_state, tree_position = lines[i].split(' ', 1)
            # take line and get content of the braces in the line with a regex and convert to json
            pos1 = lines[i].find('{')
            pos2 = lines[i].rfind('}')

            json_data = json.loads(lines[i][pos1:pos2+1])
            #json_data['depth'] as integer

            if json_data['state'] == "1" and int(json_data['depth']) <= 3:
                
                data.append({
                    'visibility_state': int(visibility_state),
                    'tree_position': tree_position.strip(),
                    'json_data': json_data
                })
            
            if json_data['name'].find(cameraname) > -1:
                camera = np.array([[json_data['c_00'], json_data['c_01'], json_data['c_02'], json_data['c_03']],
                                   [json_data['c_10'], json_data['c_11'], json_data['c_12'], json_data['c_13']],
                                   [json_data['c_20'], json_data['c_21'], json_data['c_22'], json_data['c_23']],
                                   [json_data['c_30'], json_data['c_31'], json_data['c_32'], json_data['c_33']]])

            
            
    return data, camera



def transform_vector(matrix, json_str):
    # Parse the JSON string to get the vector values
    data = json.loads(json_str)
    vector = np.array([data['x'], data['y'], data['z'], 1])

    # Perform the matrix transformation
    

    # Return the transformed vector
    return transformed_vector


def applyMatrix4x4(matrix, vector):
    # Create a 4x1 matrix from the vector
    vector = np.array([vector[0], vector[1], vector[2], 1])

    #TODO: const w = 1 / ( e[ 3 ] * x + e[ 7 ] * y + e[ 11 ] * z + e[ 15 ] );
    #This calculates the inverse of the w component after the transformation.
    # In homogeneous coordinates (used in 3D graphics for matrix transformations), 
    #the w component is used for perspective transformations. This calculation effectively applies 
    #the perspective division part of the transformation, where the w component is used to scale the x, y, and z components 
    #back to their proper perspective.

    # Perform the matrix multiplication
    transformed_vector = np.dot(matrix, vector)

    # Return the transformed vector
    return transformed_vector

def getObjectsFromInput(inputs):
    objects = []
    for i in range(0, len(inputs), 1):
        #if inputs[i]['json_data']['m_Name'] != "Main Camera":
        objects.append(Vector3(float(inputs[i]['json_data']['t_x']), float(inputs[i]['json_data']['t_y']), float(inputs[i]['json_data']['t_z']), inputs[i]['json_data']['path']))
    return objects

class Plane:
    def __init__(self, normal):
        self.normal = normal

    def project_on_plane(self, vector):
        # Implement the projection of the vector onto the plane defined by the plane's normal
        distance = np.dot(vector, self.normal) / np.linalg.norm(self.normal)
        projection = vector - distance * self.normal
        return projection

# 	return super.getWorldDirection( target ).negate();
#		this.updateWorldMatrix( true, false );
#
#		const e = this.matrixWorld.elements;
#
#		return target.set( e[ 8 ], e[ 9 ], e[ 10 ] ).normalize();


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
    def __init__(self, x, y, z, name=None):
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
    
    #[
   # 1.0078700806456729,
   # 0,
   # 0,
   # 0,
        
   # 0,
   # 1.3032253728412058,
   # 0,
   # 0,
        
   # 0,
   # 0,
   # -1.0002000200020003,
   # -1,
        
   # 0,
   # 0,
   # -0.20002000200020004,
   # 0
    #]
        

    # Eine einfache Projektionsmethode, die hier nicht vollständig definiert ist
    def project(self, camera):
        camera_inverse = np.linalg.inv(camera)
        camera_projection =  np.array([[1.0078700806456729, 0, 0, 0],
                                [0, 1.3032253728412058, 0, 0],
                                [0, 0, -1.0002000200020003, -1],
                                [0, 0, -0.20002000200020004, 0]])
        tmp = applyMatrix4x4(camera_inverse, [self.x, self.y, self.z])
        tmp = applyMatrix4x4(camera_projection, [tmp[0], tmp[1], tmp[2]])
        return Vector3(tmp[0], tmp[1], tmp[2],self.name) 
        

def compare_positions(objA, objB):
    left_right = "links" if objA.x < objB.x else "rechts"
    left_right = left_right if abs(objA.x - objB.x) > 0.01 else "selbe ebene"
    above_below = "unter" if objA.y < objB.y else "über"
    above_below = above_below if abs(objA.y - objB.y) > 0.01 else "selbe höhe"
    front_back = "vor" if objA.z < objB.z else "hinter"
    front_back = front_back if objA.z != objB.z else "selbe Tiefe"

    print(f"\n Objekt {objA.name} ist {left_right} von Objekt {objB.name} und {above_below} Objekt {objB.name} und {front_back} Objekt {objB.name}.")

def determine_arrangement2(camera, objects):
    #obj1PositionInCameraSpace = objects[0].project(camera)
    #obj2PositionInCameraSpace = objects[1].project(camera)
    #obj3PositionInCameraSpace = objects[2].project(camera)

    #compare_positions(obj1PositionInCameraSpace, obj2PositionInCameraSpace)
    #compare_positions(obj2PositionInCameraSpace, obj3PositionInCameraSpace)
    #compare_positions(obj1PositionInCameraSpace, obj3PositionInCameraSpace)
    #compare_positions(obj2PositionInCameraSpace, obj1PositionInCameraSpace)
    #compare_positions(obj3PositionInCameraSpace, obj2PositionInCameraSpace)
    #compare_positions(obj3PositionInCameraSpace, obj1PositionInCameraSpace)
    for i in range(len(objects)):
        objInCameraSpace = objects[i].project(camera)
        for j in range(len(objects)):
            if i != j:
                compare_positions(objInCameraSpace, objects[j].project(camera))


#def determine_arrangement(camera, objects):
#    # Assuming 'camera' has a method 'get_world_direction()' that returns a NumPy array
#    direction = get_camera_direction(camera, np.array([0, 0, 0]))
#
#    # Create a plane perpendicular to the camera direction
#    plane = Plane(direction)
#
#    points = []
#    for object in objects:
#        object_position = object  # Assuming 'object.position' is a list or tuple
#        projected_point = plane.project_on_plane(object_position)
#        points.append(projected_point)
#
#    threshold = 0.1
#    x1_are_side_by_side = abs(points[0][0] - points[1][0]) > threshold
#    x2_are_side_by_side = abs(points[0][0] - points[2][0]) > threshold
#    x3_are_side_by_side = abs(points[1][0] - points[2][0]) > threshold
#
#    x1_are_up_down = abs(points[0][2] - points[1][2]) > threshold
#    x2_are_up_down = abs(points[0][2] - points[2][2]) > threshold
#    x3_are_up_down = abs(points[1][2] - points[2][2]) > threshold
#
#    print("x1 Die Objekte g,r sind up down." if x1_are_up_down else "x1 Die Objekte g,r sind same.",
#          "x2 Die Objekte g,b sind up down." if x2_are_up_down else "x2 Die Objekte g,b sind same.",
#          "x3 Die Objekte r,b sind up down." if x3_are_up_down else "x3 Die Objekte r,b sind same.")
#

# Position der Kamera
# camera.position.set(0, 0, 100);

#  object1.position.set(-10, 0, 0);
#  object2.position.set(0, 0, 0);
#  object3.position.set(0, 0, 10);

# create a vector -10,0,0
# create a vector 0,0,0
# create a vector 0,0,10
    


#object1 = np.array([-10, 0, 0])
#object2 = np.array([0, 0, 0])
#object3 = np.array([0, 0, 10])

object1 = Vector3(-10, 0, 0, "Couch_1")
object2 = Vector3(0, 0, 0, "Kühlschrank_1")
object3 = Vector3(0, 0, 10, "Mensch_1")
object4 = Vector3(10, 0, 0, "Lampe_1")

#[
#    1,
#    0,
#    0,
#    0,

#    0,
#    1,
#    -6.123233995736766e-17,
#    0,

#    0,
#    6.123233995736766e-17,
#    1,
#    0,

#    0,
#    6.123233995736766e-15,
#    100,
#    1
#]

# creae a 4x4 matrix
camera = np.array([[1, 0, 0, 0],
                   [0, 1, -6.123233995736766e-17, 0],
                   [0, 6.123233995736766e-17, 1, 0],
                   [0, 6.123233995736766e-15, 100,1]])



#objects = [object1, object2, object3, object4]

inputs, camera = filter_log_file("input_data/scenegraphlog3.log", "Main Camera")


#print(inputs)

objects = getObjectsFromInput(inputs)

#print(objects)

determine_arrangement2(camera, objects)
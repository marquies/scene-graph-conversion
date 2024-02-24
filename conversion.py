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



def transform_vector(matrix, json_str):
    # Parse the JSON string to get the vector values
    data = json.loads(json_str)
    vector = np.array([data['x'], data['y'], data['z'], 1])

    # Perform the matrix transformation
    

    # Return the transformed vector
    return transformed_vector



def getObjectsFromInput(inputs):
    objects = []
    for i in range(0, len(inputs), 1):
        #if inputs[i]['json_data']['m_Name'] != "Main Camera":
        objects.append(Vector3(float(inputs[i]['json_data']['t_x']), float(inputs[i]['json_data']['t_y']), float(inputs[i]['json_data']['t_z']), inputs[i]['json_data']['path']))
    return objects

class Camera:
    def __init__(self, position, projection_matrix):
        self.position = position
        self.projection_matrix = projection_matrix
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
    
        

    # Eine einfache Projektionsmethode, die hier nicht vollständig definiert ist
    def project(self, camera):
        camera_inverse = np.linalg.inv(camera.position)
        #camera_projection =  np.array([[1.0078700806456729, 0, 0, 0],
        #                        [0, 1.3032253728412058, 0, 0],
        #                        [0, 0, -1.0002000200020003, -1],
        #                        [0, 0, -0.20002000200020004, 0]])
        camera_projection = camera.projection_matrix
        tmp = self.applyMatrix4x4(camera_inverse)#, [self.x, self.y, self.z])
        tmp = self.applyMatrix4x4(camera_projection)#, tmp)
        return tmp #Vector3(tmp[0], tmp[1], tmp[2],self.name) 

    def applyMatrix4x4(self, matrix):#, vector):
        # Create a 4x1 matrix from the vector
    
        #TODO: const w = 1 / ( e[ 3 ] * x + e[ 7 ] * y + e[ 11 ] * z + e[ 15 ] );
        #This calculates the inverse of the w component after the transformation.
        # In homogeneous coordinates (used in 3D graphics for matrix transformations), 
        #the w component is used for perspective transformations. This calculation effectively applies 
        #the perspective division part of the transformation, where the w component is used to scale the x, y, and z components 
        #back to their proper perspective.
    
        x = self.x
        y = self.y
        z = self.z
        w = 1 / ( matrix[3][0] * x + matrix[3][1] * y + matrix[3][2] * z + matrix[3][3] )
        
        self.x = ( matrix[ 0 ][0] * x + matrix[0][1] * y + matrix[0][2] * z +  matrix[0][3] ) * w
        self.y = ( matrix[ 1 ][0] * x + matrix[1][1] * y + matrix[1][2] * z +  matrix[1][3] ) * w
        self.z = ( matrix[ 2 ][0] * x + matrix[2][1] * y + matrix[2][2] * z +  matrix[2][3] ) * w

        #vector = np.array([vector[0], vector[1], vector[2], 1])
        # Perform the matrix multiplication
        #transformed_vector = np.dot(matrix, vector)
    
        # Return the transformed vector
        return self         
    
def compare_positions(objA, objB):
    left_right = "links" if objA.x < objB.x else "rechts"
    left_right = left_right if abs(objA.x - objB.x) > 0.01 else "selbe ebene"
    above_below = "unter" if objA.y < objB.y else "über"
    above_below = above_below if abs(objA.y - objB.y) > 0.01 else "selbe höhe"
    front_back = "vor" if objA.z < objB.z else "hinter"
    front_back = front_back if abs(objA.z - objB.z) > 0.01 else "selbe Tiefe"

    print(f"\n Objekt {objA.name} ist {left_right} von Objekt {objB.name} und {above_below} Objekt {objB.name} und {front_back} Objekt {objB.name}.")

def determine_arrangement2(camera, objects):
    for i in range(len(objects)):
        objInCameraSpace = objects[i].project(camera)
        for j in range(len(objects)):
            if i != j:
                compare_positions(objInCameraSpace, objects[j].project(camera))


    


# creae a 4x4 matrix
#camera = np.array([[1, 0, 0, 0],
#                   [0, 1, -6.123233995736766e-17, 0],
#                   [0, 6.123233995736766e-17, 1, 0],
#                   [0, 6.123233995736766e-15, 100,1]])


inputs, camera = filter_log_file("input_data/scenegraphlog3.log", "Main Camera")


#print(inputs)

objects = getObjectsFromInput(inputs)

#print(objects)

determine_arrangement2(camera, objects)
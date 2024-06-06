import math
import rospy
from gazebo_msgs.msg import ModelStates
from std_msgs.msg import Int8
from gazebo_msgs.srv import SetModelState
from gazebo_msgs.msg import ModelState
from scipy.spatial.transform import Rotation as R

class ProximityChecker:
    """
    Class to check the proximity between the robot and the human.
    The class receives the robot position and the human position
    and checks if the distance between them is less than the threshold.
    If the distance is less than the threshold, the human model is moved
    to the next position. The class is used to check if the task is completed
    and to manipulate it.
    """
    
    def __init__(self):

        self.distance = 100
        rospy.init_node('proximity_checker', anonymous=True)

        # Define the human model position in the simulation
        self.human_poses = {
            'pos_0': [7.07424, -2.47124, -0.319319, 0, 0, -1.605274],
            'pos_1': [7.300846, 5.64267, -0.319319, 0, 0, 0], 
            'pos_2': [-0.656005, 5.095052, -0.319319, 0, 0, 1.559867], 
            'pos_3': [-0.287133, -0.470007, -0.303000, 0, 0, -3.138091], 
            'pos_4': [-7.084292, -0.514416, -0.303000, 0, 0, 1.526374], 
            'pos_5': [-6.187724, -6.035108, -0.319319, 0, 0, 3.133769], 
            'pos_6': [1.458310, -5.335922, -0.319319, 0, 0, -1.529479], 
            'pos_7': [0.552367, -10.920881, -0.319319, 0, 0, 3.087480] 
        }
        
        # Initialize the variables
        self.proximity_threshold = 1
        self.initialpose = 0
        self.robot_position = ModelState().pose.position
        self.robot_position.x = 0
        self.robot_position.y = 0
        self.index = None

        # Get the first human position
        human, pose = list(self.human_poses.items())[self.initialpose]
        self.pose_x = pose[0]
        self.pose_y = pose[1]

        # Subscribe to the model states topic to check the robot position in the world
        rospy.Subscriber("/gazebo/model_states", ModelStates, self.model_states_callback)

        # Wait for the service to set the model state (to move the human model)
        rospy.wait_for_service('/gazebo/set_model_state')
        self.set_model_state = rospy.ServiceProxy('/gazebo/set_model_state', SetModelState)

        # Publish the task completed topic
        self.task_completed=rospy.Publisher("task_completed", Int8, queue_size=10)
    
    

    def move_model(self, model_name, step=0):
        """
        Function to move the human model to the next position.
        The function receives the model name and the step (human model
        number) to move the model to the next position.
        """
        print("Trying to move the human model to the next position...")
        print("Step: ", step)

        # Create the message to set the model state
        state_msg = ModelState()  
        state_msg.model_name = model_name
        state_msg.pose.position.x = self.human_poses[f'pos_{step}'][0]  # x
        state_msg.pose.position.y = self.human_poses[f'pos_{step}'][1]  # y
        state_msg.pose.position.z = self.human_poses[f'pos_{step}'][2]  # z
        
        # Get the Euler angles from the human poses
        roll = self.human_poses[f'pos_{step}'][3]
        pitch = self.human_poses[f'pos_{step}'][4]
        yaw = self.human_poses[f'pos_{step}'][5]
        
        # Create a Rotation object from Euler angles
        rotation = R.from_euler('xyz', [roll, pitch, yaw])
        
        # Convert the rotation to a quaternion
        quaternion = rotation.as_quat()
        
        # Fill the orientation in the message with the quaternion
        state_msg.pose.orientation.x = quaternion[0]
        state_msg.pose.orientation.y = quaternion[1]
        state_msg.pose.orientation.z = quaternion[2]
        state_msg.pose.orientation.w = quaternion[3]

        # Print the new human position (no info given to the human detection node)
        print("New human position: ", state_msg.pose.position.x, state_msg.pose.position.y, state_msg.pose.position.z)
        self.set_model_state(state_msg)


    def model_states_callback(self, data):
        """
        Callback function for the model states topic.
        The function receives the model states from the simulation
        and saves the robot position in the class variable.
        """   
        # Get the index of the husky model in the model states message
        if self.index is None:
            for name in data.name:
                if name == "husky_model":
                    self.index = data.name.index(name)
                    #print("Index: ", self.index)
                    break

        else:
        # Save the robot position
            self.robot_position = data.pose[self.index].position

        # Check the proximity between the robot and the human
        self.check_proximity()


    def check_proximity(self):
        """
        Function to check the proximity between the robot and the human.
        The function calculates the distance between the robot and the human
        and if the distance is less than the threshold, the human model is moved
        to the next position.
        """
        # Check if the initialpose is greater than 7 (all the human positions)
        if self.initialpose > 7:
            return 0

        # Calculate the distance between the robot and the human (euclidean distance)
        distance = math.sqrt((self.robot_position.x - self.pose_x)**2 + (self.robot_position.y - self.pose_y)**2)

        # Check if the distance is less than the threshold
        if distance < self.proximity_threshold:
            print("Proximity detected!")
            # Increment the initialpose to move the human model to the next position
            self.initialpose=self.initialpose+1

            if self.initialpose > len(self.human_poses):
                # Publish the task completed topic
                self.task_completed.publish(1)
                return 0
            
            # Get the next human x and y coordinates for the next euclidean distance calculation
            human, pose = list(self.human_poses.items())[self.initialpose]
            self.pose_x = pose[0]
            self.pose_y = pose[1]
            # Move the human model to the next position
            self.move_model('person_standing', step=self.initialpose)

        else:
            pass

if __name__ == "__main__":
    proximitychecker=ProximityChecker()
    rospy.spin()
    
                




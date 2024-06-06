import rospy
from geometry_msgs.msg import Twist, PointStamped  
from std_msgs.msg import Int8
import sys

class RobotControl:
    def __init__(self):
        rospy.init_node('robot_control', anonymous=True)
        # Start to publish the movement finished topic and the cmd_vel topic to control the model wheels
        self.movement_finished= rospy.Publisher("/movement_finished", Int8, queue_size=10)
        self.cmd_vel_pub = rospy.Publisher("/husky_model/husky/cmd_vel", Twist, queue_size=10)

        # Subscribe to the error coordinates topic
        self.image_sub = rospy.Subscriber("/yolo_human_detection/human_coordinates",PointStamped, queue_size=10,callback=self.control_loop)

        # Initialize the variables
        self.target_detected = False
        self.human_position = None
        self.moving=False
        # Wait for all the nodes to start
        rospy.sleep(1)

        # Notify the camera node that the robot control node is ready to get the coordinates
        self.movement_finished.publish(1)
        print("Robot control node started")

        # Subscribe to the task_completed topic to exit the node
        rospy.Subscriber("task_completed", Int8, self.task_completed_callback)
        
    def task_completed_callback(self, data):
        """
        Callback function for the task_completed topic,
        once the task is completed (notified from the
        topic in the task manager), the node will exit.
        """
        try:
            sys.exit("Task completed. Exiting...")
        except:
            print("Task completed.")
            return 0
       

        

    def control_loop(self, coordinate_msg):
        """
        Callback function for the error coordinates topic.
        The function receives the error coordinates from the camera node
        and moves the robot based on the error.
        """

        # Check if the robot is already moving to avoid multiple messages
        if not self.moving:
            self.moving=True
            error_x=coordinate_msg.point.x
            error_y=coordinate_msg.point.y
            cmd = Twist()

            # Verify if the human is detected
            if coordinate_msg.point.x == 1000 and coordinate_msg.point.y == 1000:
                self.target_detected = False

            else:
                self.target_detected = True

            # Move the robot based on the error coordinates
            if self.target_detected:

                # Center the human in the image
                if abs(error_x) > 20:  
                    cmd.angular.z = -0.05 * error_x  # Ruota per centrare l'umano
                    cmd.linear.x = 1

                # Get closer to the human (move forward)
                else:
                    cmd.linear.x = 1  
                    cmd.angular.z = 0
                print(f"Error: {error_x}, {error_y}")


            elif not self.target_detected:
                # If the human is not detected, rotate on itself
                cmd.angular.z = 1.5  
                cmd.linear.x = 0

            # Publish the command to move the robot
            self.cmd_vel_pub.publish(cmd)
            # Notify the camera node that the robot has finished the movement
            self.movement_finished.publish(1)
            self.moving=False
        

def main():
    #sleep for 5 seconds to wait for the other nodes to start
    
    rospy.sleep(5)
    
    robot_control = RobotControl()
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")

if __name__ == '__main__':
    main()

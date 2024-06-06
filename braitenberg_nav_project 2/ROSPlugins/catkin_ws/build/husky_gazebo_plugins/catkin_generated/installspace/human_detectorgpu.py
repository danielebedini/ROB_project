import rospy
from sensor_msgs.msg import Image
from geometry_msgs.msg import  PointStamped
from std_msgs.msg import Int8
from cv_bridge import CvBridge, CvBridgeError
from ultralytics import YOLO
import cv2
import sys
import torch


# Verify if the device supports MPS (Multi-Process Service) and set the device accordingly
if torch.backends.mps.is_available():
    device = torch.device("mps")
else:
    device = torch.device("cpu")

model = torch.hub.load('ultralytics/yolov5', 'yolov5n').to(device)  # yolov5n per nano
#model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True).to(device)


class YOLOHumanDetection:
    def __init__(self):
        self.bridge = CvBridge()
        rospy.init_node('yolo_human_detection', anonymous=True)

        # Start to subscribe to the camera topic and the notifier
        self.image_sub = rospy.Subscriber("/husky_model/husky/camera", Image, self.image_callback)
        self.move_finished_sub = rospy.Subscriber("/movement_finished", Int8, self.move_finished_callback)
        print("Subscribed to movement_finished topic")

        # Start to publish the human coordinates and the image with the rectangle
        self.coordinate_pub = rospy.Publisher("/yolo_human_detection/human_coordinates", PointStamped, queue_size=10)
        self.rectangle_pub = rospy.Publisher("/yolo_human_detection/human_rectangle1", Image, queue_size=10)
        print("Topics published")

        # Subscribe to the task_completed topic
        rospy.Subscriber("task_completed", Int8, self.task_completed_callback)

        # Initialize the variables
        self.target_detected = False
        self.human_position = None
        self.image_width = None
        self.image_height = None
        self.latest_image = None
            
    def task_completed_callback(self, data):
        """
        Callback function for the task_completed topic,
        once the task is completed (notified from the 
        topic in the task manager), the node will exit.
        """
        sys.exit("Task completed. Exiting...")

    def image_callback(self,msg):
        """
        Callback function for the image topic.
        The function receives the image from the camera
        and save it in the latest_image variable.
        """
        try:
            self.latest_image = msg
        except CvBridgeError as e:
            rospy.logerr(f"Error in the image conversion: {e}")


    def move_finished_callback(self,data):
            """
            Callback function for the movement_finished topic.
            The function receives the message from the movement
            manager when it ends the previous one of the next timestep
            and starts the human detection.
            """
            print("Received message finished")
            try:
                original_image = self.bridge.imgmsg_to_cv2(self.latest_image, "bgr8")
            except CvBridgeError as e:
                print(e)
                return
            # Resize the image to 3/5 of the original height (less computation)
            original_height = original_image.shape[0]  # Ottieni l'altezza dell'immagine originale
            newheight = original_height * 3 // 5
            roi = original_image[:newheight, :]
            preprocessed_image = roi.copy()

            # Save the resized image width and height in the class variable
            if self.image_width is None or self.image_height is None:
                self.image_height, self.image_width, _ = preprocessed_image.shape
                
            # Human detection with YOLO
            if self.latest_image is not None:
                results = model(preprocessed_image)
                self.target_detected = False
                person_detections = [det for det in results.pred[0] if det[-1] == 0]  # '0' è l'ID per "person" in COCO dataset
                if person_detections:
                    print("Human detected!")
                    for detection in person_detections:
                        x1, y1, x2, y2, conf, cls = detection
                        self.target_detected = True
                        self.human_position = ((int(x1) + int(x2)) // 2, (int(y1) + int(y2)) // 2)
                        cv2.rectangle(preprocessed_image, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)

            # Publish the image with the rectangle if a human is detected
            annotated_image_msg = self.bridge.cv2_to_imgmsg(preprocessed_image, encoding='bgr8')
            self.rectangle_pub.publish(annotated_image_msg)

                # Publish the error between the human position and the center of the image
            if self.target_detected:
                print(f"Human detected at {self.human_position}")
                human_error = PointStamped()
                human_error.point.x = self.human_position[0] - (self.image_width // 2)
                human_error.point.y = self.human_position[1] - (self.image_height // 2)
                self.coordinate_pub.publish(human_error)

                # If no human is detected, publish a point with x=1000 and y=1000
            else:
                print("No human detected")
                human_error = PointStamped()
                human_error.point.x = 1000
                human_error.point.y = 1000
                self.coordinate_pub.publish(human_error)
            

def main():
    rospy.init_node('yolo_human_detection', anonymous=True)
    yolo_human_detection = YOLOHumanDetection()
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")


if __name__ == '__main__':
    main()

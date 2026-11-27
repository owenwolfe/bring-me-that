'''
	Name:
		Jonathan Ortiz Guzman
	Project:
		Robotics Final Project
	Description:
		A script that connects ROS2 with YOLO from Ultralytics. This
		was tested on a Jetson Orin Nano with a virtual Python 3.10.12
		environment. The model is a YOLO26 for object detection. 
		Followed and modified the official Ultralytics documentation
		for "YOLO with ROS Quickstart".
		Receives compressed images from the ROS topic to prevent 
		delay with large frame data but able to restore after receiving.


	Requirements:
		numpy 1.26.4
'''
import cv_bridge
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import CompressedImage
from rclpy.qos import qos_profile_sensor_data

from ultralytics import YOLO

class Image_Subscriber(Node):
	def __init__(self):
		'''Initialize the ROS2 node and image interfaces'''
		super().__init__("image_subscriber")
		self.bridge = cv_bridge.CvBridge()
		self.subscription = self.create_subscription(CompressedImage, '/camera/image_compressed', self.image_callback, qos_profile_sensor_data)

		self.model = YOLO("train1.pt")


	def image_callback(self, message):
		'''Save camera frame image'''
		frame = self.bridge.compressed_imgmsg_to_cv2(message, desired_encoding="bgr8") # A numpy array retured

		# Make prediction of object detection
		results = self.model.predict(source=frame, device=0)

		# DEBUG
		self.get_logger().info(f"received frame: {frame.shape}, detections: {len(results[0].boxes)}")


def main(args=None):
	'''Start the ROS2 node'''
	rclpy.init(args = args)
	node = Image_Subscriber()
	rclpy.spin(node) # Keeps ROS communication alive

	node.destroy_node()
	rclpy.shutdown()

if __name__ == "__main__":
	main()

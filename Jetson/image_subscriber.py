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
		for "YOLO with ROS Quickstart"

	Requirements:
		numpy 1.26.4
'''
import cv_bridge
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from rclpy.qos import qos_profile_sensor_data

class Image_Subscriber(Node):
	def __init__(self):
		'''Initialize the ROS2 node and image interfaces'''
		super().__init__("image_subscriber")
		self.bridge = cv_bridge.CvBridge()
		self.subscription = self.create_subscription(Image, '/camera/image_raw', self.image_callback, qos_profile_sensor_data)

	def image_callback(self, message):
		'''Save camera frame image'''
		frame = self.bridge.imgmsg_to_cv2(message, desired_encoding="bgr8")

		# DEBUG
		self.get_logger().info(f"received frame: {frame.shape}")


def main(args=None):
	'''Start the ROS2 node'''
	rclpy.init(args = args)
	node = Image_Subscriber()
	rclpy.spin(node) # Keeps ROS communication alive

	node.destroy_node()
	rclpy.shutdown()

if __name__ == "__main__":
	main()

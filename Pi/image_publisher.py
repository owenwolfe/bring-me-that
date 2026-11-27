'''
        Name:
                Jonathan Ortiz Guzman
        Project:
                Robotics Final Project
        Description:
                A script that connects ROS2 with YOLO from Ultralytics. This
                file is intended for an Ubuntu 22.04 with ROS2 and Python 3.10.12
                environment. The model is a YOLO26 for object detection.
                Followed and modified the official Ultralytics documentation
                for "YOLO with ROS Quickstart"

'''
import cv_bridge
import rclpy
from rclpy.node import Node
#from rclpy.qos import qos_profile_sensor_data #FOR BEST_EFFORT
from rclpy.qos import QoSProfile, ReliabilityPolicy
from sensor_msgs.msg import Image
import cv2

class Image_Publisher(Node):
	'''Passes camera frames to Jetson for processing'''
	def __init__(self):
		'''Initialize the ROS2 node, and opencv camera processing'''
		super().__init__("image_publisher")


		qos = QoSProfile(depth=10, reliability=ReliabilityPolicy.RELIABLE)
		self.publisher = self.create_publisher(Image, "/camera/image_raw", qos)
		self.bridge = cv_bridge.CvBridge()

		# OpenCV implementation for camera loading
		self.camera = cv2.VideoCapture(0)
		self.timer = self.create_timer(0.01, self.publish_frame) # 1 second for 10 frames

	def publish_frame(self):
		ret, frame = self.camera.read()

		if not ret:
			self.get_logger().warning("Failed to get camera frame")
			return

		message = self.bridge.cv2_to_imgmsg(frame, encoding="bgr8")
		self.publisher.publish(message)


def main(args=None):
	rclpy.init(args=args)
	node = Image_Publisher()

	try:
		rclpy.spin(node)
	finally:
		node.camera.release()
		node.destroy_node()
		rclpy.shutdown()

if __name__ == "__main__":
	main()

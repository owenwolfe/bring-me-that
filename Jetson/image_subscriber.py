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
import cv2

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

		# Section dervived from https://www.geeksforgeeks.org/computer_vision/object-detection-with-yolo-and-opencv/
		# Display boxes per detected object in each frame
		for result in results:
			class_names = result.names
			for box in result.boxes:
				if box.conf[0] > 0.4: # Only 40% or higher in confidence will be shown
					x1,y1,x2,y2 = map(int, box.xyxy[0])

					cls = int(box.cls[0])
					class_name = class_names[cls]
					conf = float(box.conf[0])
					box_color = (255,0,0) # BGR
					cv2.rectangle(frame, (x1,y1), (x2,y2), box_color, 2)
					cv2.putText(frame, f"{class_name} {conf:.2f}", (x1, max(y1 - 10, 20)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, box_color, 2)

		########## DEBUG #########
                # Display Video Frame
		cv2.imshow('Live Camera Feed', frame)
		cv2.waitKey(1)
		self.get_logger().info(f"received frame: {frame.shape}, detections: {len(results[0].boxes)}")
		#self.get_logger().info(f"received frame: {frame.shape}")


def main(args=None):
	'''Start the ROS2 node'''
	rclpy.init(args = args)
	node = Image_Subscriber()
	rclpy.spin(node) # Keeps ROS communication alive

	node.destroy_node()
	rclpy.shutdown()
	cv2.destroyAllWIndows()

if __name__ == "__main__":
	main()

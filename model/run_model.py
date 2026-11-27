'''
  Name: 
    Jonathan Ortiz Guzman
  Created: 
    November 23, 2026
  Description:
    Runs exported .pt file for a custom pretrained model
    focused on tennis balls. This file is for Nvidia Jetson
    Orin Nano that has python 3.10.12. 


'''
from ultralytics import YOLO
import cv2
import os



# Loads the model to be connected with the Logitech USB Camera
model = YOLO("train1.pt")

# Live camera dervied from: https://www.geeksforgeeks.org/python/python-opencv-capture-video-from-camera/
cam = cv2.VideoCapture(0)

while True:
	ret, frame = cam.read()

	if not ret:
		break

	results = model.predict(source=frame, device=0) #Webcam with CUDA GPU

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

	cv2.imshow('Live Camera Feed', frame)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

cam.release()
cv2.destroyAllWindows()

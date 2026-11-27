# bring-me-that

## Description

Dynamixel OpenManipulatorX Setup Commands

- https://docs.robotis.com/docs/systems/openmanipulator_x/quick_start_guide/?ros=humble

- There is an error with the moveit debugging python package. To resolve, do the following:
  ```bash
  sudo dpkg --remove ros-humble-moveit-py-dbgsym
  sudo dpkg --remove ros-humble-moveit-py
  sudo apt --fix-broken install
  sudo dpkg --configure -a
  ```

iRobot Create 3 Setup Commands

- https://iroboteducation.github.io/create3_docs/setup/ubuntu2204/


Running YOLO26 Tennis Bal Detection Model:
- Have a python 3.10.12 virtual environment
- Have Ultralytics python module installed
- Have Jetpack configured (if using Jetson)
- Have camera connected to device
- Run 'run_model.py'

## Notes
- In addition to the Pi publisher script, the following command has to be run in a separate terminal on the Pi to convert the raw image data to the compresssed image data format: 
```bash
ros2 run image_transport republish raw in:=/camera/image_raw compressed out/compressed:=/camera/image_compressed
```

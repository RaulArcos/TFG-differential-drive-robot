#!/bin/bash

echo "Compiling RobotUcaDetector module..."
cd /home/robot/robotuca/modules/detector
python setup.py sdist bdist_wheel
sudo pip install .

sudo cp -r /usr/local/lib/python3.8/dist-packages/RobotUcaDetector /usr/lib/python3.8/dist-packages/RobotUcaDetector
echo "RobotUcaDetector module installed!"

echo "Compiling RobotUcaVideo module..."
cd /home/robot/robotuca/modules/video
if [ -d "build" ]; then
  rm -r build
fi
cmake -B build -H. -G "Unix Makefiles"
cd build
make -j6

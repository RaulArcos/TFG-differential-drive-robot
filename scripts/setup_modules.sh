#!/bin/bash

module_to_compile="$1"

compile_detector() {
  echo "Compiling RobotUcaDetector module..."
  cd /home/robot/robotuca/modules/detector
  python setup.py sdist bdist_wheel
  sudo pip install .
  sudo cp -r /usr/local/lib/python3.8/dist-packages/RobotUcaDetector /usr/lib/python3.8/dist-packages/RobotUcaDetector
  echo "RobotUcaDetector module installed!"
}

compile_video() {
  echo "Compiling RobotUcaVideo module..."
  cd /home/robot/robotuca/modules/video
  if [ -d "build" ]; then
    rm -r build
  fi
  cmake -B build -H. -G "Unix Makefiles"
  cd build
  make -j6
  echo "RobotUcaVideo module installed!"
}

compile_web() {
  echo "Compiling RobotUcaWeb module..."
  cd /home/robot/robotuca/modules/web
  python setup.py sdist bdist_wheel
  sudo pip install .
  sudo cp -r /usr/local/lib/python3.8/dist-packages/RobotUcaWeb /usr/lib/python3.8/dist-packages/RobotUcaWeb
  echo "RobotUcaWeb module installed!"
}

if [ "$module_to_compile" = "detector" ]; then
  compile_detector
elif [ "$module_to_compile" = "video" ]; then
  compile_video
elif [ "$module_to_compile" = "web" ]; then
  compile_web
elif [ "$module_to_compile" = "all" ] || [ -z "$module_to_compile" ]; then
  compile_detector
  compile_video
  compile_web
else
  echo "Invalid module specified. Usage: $0 [detector|video|web|all]"
fi
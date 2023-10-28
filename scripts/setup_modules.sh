#!/bin/bash

cd /home/robot/workspace/robotuca/modules/detector
python setup.py sdist bdist_wheel
sudo pip install .

sudo cp -r /usr/local/lib/python3.8/dist-packages/RobotUcaDetector /usr/lib/python3.8/dist-packages/RobotUcaDetector
from setuptools import setup
import setuptools.command.build_py
import os
import subprocess
import sys

import distutils.core

NAME='robotUcaWeb'
VERSION='0.1.0'
DESCRIPTION='RobotUca WEB interface module'
AUTHOR='Raúl Arcos Herrera'
EMAIL='raularcosherrera@gmail.com'
LICENSE=''
PACKAGES=['RobotUcaWeb']


class BuildPyCommand(setuptools.command.build_py.build_py):
    """Custom build command."""
    def run(self):
      """Run command."""
      command = ['npx', 'rollup', '--config', '--bundleConfigAsCjs']
      # command.append(os.getcwd())
      self.announce(
         'Running command: %s' % str(command),
         level=distutils.log.INFO)
      origWD = os.getcwd() # remember our original working directory

      os.chdir(os.path.join(os.path.abspath(sys.path[0]), 'RobotUcaWeb/html/js'))
      subprocess.check_call(command)
      os.chdir(origWD)
      setuptools.command.build_py.build_py.run(self)

setup(name=NAME,
   version=VERSION,
   description=DESCRIPTION,
   author=AUTHOR,
   author_email=EMAIL,
   license=LICENSE,
   packages=PACKAGES,
   zip_safe=False,
   # cmdclass={
   #    'build_py': BuildPyCommand,
   # },
   data_files=[('html', ['RobotUcaWeb/html/css/robotuca.css', 
                  'RobotUcaWeb/html/index.html']),
               ('html/js', ['RobotUcaWeb/html/js/ros.js',
                            'RobotUcaWeb/html/js/websocket.js',
                            'RobotUcaWeb/html/js/bootstrap.bundle.min.js', 
                            'RobotUcaWeb/html/js/background.js',
                            'RobotUcaWeb/html/js/ros_src/easeljs.min.js',
                            'RobotUcaWeb/html/js/ros_src/eventemitter2.min.js',
                            'RobotUcaWeb/html/js/ros_src/ros2d.js',
                            'RobotUcaWeb/html/js/ros_src/roslib.min.js',])],
   include_package_data = True,
)

from setuptools import setup
import setuptools.command.build_py
import os
import subprocess
import sys

import distutils.core

NAME='RAH01Web'
VERSION='0.1.0'
DESCRIPTION='RAH-01 WEB interface module'
AUTHOR='Raúl Arcos Herrera'
EMAIL='raularcosherrera@gmail.com'
LICENSE=''
PACKAGES=['RAH01Web']


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

      os.chdir(os.path.join(os.path.abspath(sys.path[0]), 'RAH01Web/html/js'))
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
   data_files=[('html', ['RAH01Web/html/css/rah01.css', 
                  'RAH01Web/html/index.html', 'RAH01Web/html/css/all.min.css', 
                  'RAH01Web/html/css/bootstrap.min.css', 
                  'RAH01Web/html/css/font-awesome.min.css']),
               ('html/js', ['RAH01Web/html/js/ros.js',
                            'RAH01Web/html/js/websocket.js',
                            'RAH01Web/html/js/bootstrap.bundle.min.js', 
                            'RAH01Web/html/js/telemetry.js',
                            'RAH01Web/html/js/gsap.min.js',
                            'RAH01Web/html/js/control-panel.js',
                            'RAH01Web/html/js/nipple.js',
                            'RAH01Web/html/js/bootstrap.bundle.min.js',
                            'RAH01Web/html/js/charts_src/chart.js',
                            'RAH01Web/html/js/charts_src/chart-adapter-date-fns.js',
                            'RAH01Web/html/js/charts_src/chart-plugin-streaming.js',
                            'RAH01Web/html/js/ros_src/nav2d.js',
                            'RAH01Web/html/js/ros_src/easeljs.min.js',
                            'RAH01Web/html/js/ros_src/eventemitter2.min.js',
                            'RAH01Web/html/js/ros_src/ros2d.js',
                            'RAH01Web/html/js/ros_src/roslib.min.js',])],
   include_package_data = True,
)

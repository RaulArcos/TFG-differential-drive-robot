from setuptools import setup

NAME='RobotUcaDetector'
VERSION='0.0.3'
DESCRIPTION='RobotUca AI detector'
AUTHOR='GTD DSS'
EMAIL='raularcosherrera@gmail.com'
LICENSE=''
PACKAGES=['robotUcaDetector', 'robotUcaDetector.detectors']

setup(name=NAME,
   version=VERSION,
   description=DESCRIPTION,
   author=AUTHOR,
   author_email=EMAIL,
   license=LICENSE,
   packages=PACKAGES,
   zip_safe=False,
   include_package_data = True,
)

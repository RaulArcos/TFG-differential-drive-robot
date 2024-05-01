from setuptools import setup

NAME='rah01Detector'
VERSION='0.1.0'
DESCRIPTION='RAH01 IA detection module'
AUTHOR='Raúl Arcos Herrera'
EMAIL='raularcosherrera@gmail.com'
LICENSE=''
PACKAGES=['RAH01Detector']

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

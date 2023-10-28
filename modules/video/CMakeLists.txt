cmake_minimum_required(VERSION 3.16.3)

project(VideoApp
        VERSION 0.9.4
        DESCRIPTION "RobotUcaVideo Module"
        LANGUAGES CXX)

add_subdirectory (src) 

##############################################################################

set(CPACK_GENERATOR "DEB")
set(CPACK_DEBIAN_PACKAGE_NAME "robotUcaVideo")
message(STATUS "CPACK_PACKAGE_NAME: ${CPACK_PACKAGE_NAME}")
set(CPACK_DEB_COMPONENT_INSTALL ON)
set(CPACK_SET_DESTDIR TRUE)
set(CPACK_BINARY_DEB TRUE)
set(CMAKE_INSTALL_RPATH "${CMAKE_INSTALL_PREFIX}/lib")
message(STATUS "CMAKE_INSTALL_RPATH: ${CMAKE_INSTALL_PREFIX}/lib")
set(CMAKE_BUILD_WITH_INSTALL_RPATH TRUE)

set(CPACK_DEB_COMPONENT_INSTALL YES)

include(CPack)
find_program(PYTHON_EXECUTABLE python3.8)
if (PYTHON_EXECUTABLE)
    set(PYTHON_EXECUTABLE ${PYTHON_EXECUTABLE} CACHE FILEPATH "Path to Python 3.8 executable")
else()
    message(FATAL_ERROR "Python 3.8 executable not found")
endif()
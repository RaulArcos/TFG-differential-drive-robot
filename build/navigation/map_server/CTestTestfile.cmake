# CMake generated Testfile for 
# Source directory: /home/pi/rah_ws/src/navigation/map_server
# Build directory: /home/pi/rah_ws/build/navigation/map_server
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(_ctest_map_server_gtest_map_server_utest "/home/pi/rah_ws/build/catkin_generated/env_cached.sh" "/usr/bin/python2" "/opt/ros/melodic/share/catkin/cmake/test/run_tests.py" "/home/pi/rah_ws/build/test_results/map_server/gtest-map_server_utest.xml" "--return-code" "/home/pi/rah_ws/devel/lib/map_server/map_server_utest --gtest_output=xml:/home/pi/rah_ws/build/test_results/map_server/gtest-map_server_utest.xml")
set_tests_properties(_ctest_map_server_gtest_map_server_utest PROPERTIES  _BACKTRACE_TRIPLES "/opt/ros/melodic/share/catkin/cmake/test/tests.cmake;143;add_test;/opt/ros/melodic/share/catkin/cmake/test/gtest.cmake;89;catkin_run_tests_target;/opt/ros/melodic/share/catkin/cmake/test/gtest.cmake;28;_catkin_add_google_test;/home/pi/rah_ws/src/navigation/map_server/CMakeLists.txt;81;catkin_add_gtest;/home/pi/rah_ws/src/navigation/map_server/CMakeLists.txt;0;")
add_test(_ctest_map_server_rostest_test_rtest.xml "/home/pi/rah_ws/build/catkin_generated/env_cached.sh" "/usr/bin/python2" "/opt/ros/melodic/share/catkin/cmake/test/run_tests.py" "/home/pi/rah_ws/build/test_results/map_server/rostest-test_rtest.xml" "--return-code" "/usr/bin/python2 /opt/ros/melodic/share/rostest/cmake/../../../bin/rostest --pkgdir=/home/pi/rah_ws/src/navigation/map_server --package=map_server --results-filename test_rtest.xml --results-base-dir \"/home/pi/rah_ws/build/test_results\" /home/pi/rah_ws/src/navigation/map_server/test/rtest.xml ")
set_tests_properties(_ctest_map_server_rostest_test_rtest.xml PROPERTIES  _BACKTRACE_TRIPLES "/opt/ros/melodic/share/catkin/cmake/test/tests.cmake;143;add_test;/opt/ros/melodic/share/rostest/cmake/rostest-extras.cmake;52;catkin_run_tests_target;/home/pi/rah_ws/src/navigation/map_server/CMakeLists.txt;98;add_rostest;/home/pi/rah_ws/src/navigation/map_server/CMakeLists.txt;0;")
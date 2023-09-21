# CMake generated Testfile for 
# Source directory: /home/pi/rah_ws/src/diff_drive
# Build directory: /home/pi/rah_ws/build/diff_drive
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(_ctest_diff_drive_nosetests_tests "/home/pi/rah_ws/build/catkin_generated/env_cached.sh" "/usr/bin/python2" "/opt/ros/melodic/share/catkin/cmake/test/run_tests.py" "/home/pi/rah_ws/build/test_results/diff_drive/nosetests-tests.xml" "--return-code" "\"/usr/bin/cmake\" -E make_directory /home/pi/rah_ws/build/test_results/diff_drive" "/usr/bin/nosetests-2.7 -P --process-timeout=60 --where=/home/pi/rah_ws/src/diff_drive/tests --with-xunit --xunit-file=/home/pi/rah_ws/build/test_results/diff_drive/nosetests-tests.xml")
set_tests_properties(_ctest_diff_drive_nosetests_tests PROPERTIES  _BACKTRACE_TRIPLES "/opt/ros/melodic/share/catkin/cmake/test/tests.cmake;143;add_test;/opt/ros/melodic/share/catkin/cmake/test/nosetests.cmake;83;catkin_run_tests_target;/home/pi/rah_ws/src/diff_drive/CMakeLists.txt;21;catkin_add_nosetests;/home/pi/rah_ws/src/diff_drive/CMakeLists.txt;0;")

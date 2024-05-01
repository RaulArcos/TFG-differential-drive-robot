file(GLOB_RECURSE SRC_FILES *.cpp)

list(REMOVE_ITEM SRC_FILES "main.cpp")

add_executable(rah01Video main.cpp ${SRC_FILES})
find_package(PkgConfig) 
find_package (Threads)
find_package(X11 REQUIRED)
include_directories(${X11_INCLUDE_DIR})
pkg_check_modules(gst REQUIRED IMPORTED_TARGET gstreamer-1.0)
pkg_check_modules(gst-video REQUIRED IMPORTED_TARGET gstreamer-video-1.0)
pkg_check_modules(gst-controller REQUIRED IMPORTED_TARGET gstreamer-controller-1.0)
pkg_check_modules(opencv4 REQUIRED IMPORTED_TARGET opencv4)

target_compile_features(rah01Video PRIVATE cxx_std_11)

target_include_directories(rah01Video PRIVATE ../include)
target_include_directories(rah01Video PRIVATE ${GTK3_INCLUDE_DIRS} ${GST_INCLUDE_DIRS})
target_link_libraries(rah01Video
                PkgConfig::gst
                PkgConfig::gst-video
                PkgConfig::opencv4
                -lstdc++fs
                Threads::Threads
                -lv4l2
                ${GST_LIBRARIES} X11
                PkgConfig::gst-controller)

install(TARGETS rah01Video RUNTIME DESTINATION bin)


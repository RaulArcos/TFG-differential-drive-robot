#include "webcam_input.hpp"
#include "videosocket_output.hpp"
#include <chrono>
#include <thread>

using namespace robotuca;

int main (int argc, char *argv[]){
    gst_init (&argc, &argv);
    GMainLoop *loop;

    if(std::remove("/tmp/robotuca-socket-video") != 0);

    GstElement* pipeline = gst_pipeline_new ("pipeline");

    WebCamInput webcam = WebCamInput(Resolution(1280, 720));
    webcam.set_source("/dev/video0");
    VideoSocketOutput output = VideoSocketOutput(Resolution(1280, 720));
    GstElement* convert = gst_element_factory_make("videoconvert", "convert");

    gst_bin_add_many(GST_BIN(pipeline), webcam.get_bin(), output.get_bin(), convert, NULL);
    if (!gst_element_link_many(webcam.get_bin(), convert, output.get_bin(), NULL)) {
        g_warning ("Failed to link element1 and element2!");
    }

    gst_element_set_state (pipeline, GST_STATE_PLAYING);

    std::this_thread::sleep_for(std::chrono::seconds(10));
    GST_DEBUG_BIN_TO_DOT_FILE(GST_BIN(pipeline), GST_DEBUG_GRAPH_SHOW_ALL, "pipeline_after");

    loop = g_main_loop_new (NULL, TRUE);
    g_main_loop_run(loop);
    g_main_loop_unref(loop);
}
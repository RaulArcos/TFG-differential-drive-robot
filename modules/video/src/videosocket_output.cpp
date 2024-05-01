#include "videosocket_output.hpp"

using namespace rah01;

VideoSocketOutput::VideoSocketOutput(const Resolution& res){
    bin_ = gst_bin_new("video-output");

    sink_ = gst_element_factory_make("shmsink", "sink");
    capsfilter_ = gst_element_factory_make("capsfilter", "capsfilter");

    GstCaps *caps = gst_caps_new_simple("video/x-raw", 
                                        "width", G_TYPE_INT, res.width, 
                                        "height", G_TYPE_INT, res.height, 
                                        "framerate", GST_TYPE_FRACTION, 30, 1, 
                                        "format", G_TYPE_STRING, "BGRx",
                                        NULL);
    
    g_object_set(G_OBJECT(sink_), "sync", false, "wait-for-connection", false,"socket-path", "/tmp/rah01-socket-video", "perms", 511, NULL);

    g_object_set(G_OBJECT(capsfilter_), "caps", caps, NULL);

    gst_bin_add_many(GST_BIN(bin_), capsfilter_, sink_, NULL);
    if (!gst_element_link_many(capsfilter_, sink_, NULL)) {
        g_warning ("Failed to link element1 and element2!");
    }
    gst_caps_unref (caps);
    gst_element_add_pad(bin_, gst_ghost_pad_new("sink", gst_element_get_static_pad(capsfilter_, "sink")));
}

GstElement* VideoSocketOutput::get_bin() {
    return bin_;
}

#include "webcam_input.hpp"

using namespace rah01;

WebCamInput::WebCamInput(const Resolution& res){
    bin_ = gst_bin_new("cam-input");
    
    src_ = gst_element_factory_make("v4l2src", "src");
    converter_ = gst_element_factory_make("nvvidconv", "converter");
    decoder_ = gst_element_factory_make("nvv4l2decoder", "decoder");
    capsfilter_ = gst_element_factory_make("capsfilter", "capsfilter");

    GstCaps *caps = gst_caps_new_simple("image/jpeg", 
                                        "width", G_TYPE_INT, res.width, 
                                        "height", G_TYPE_INT, res.height, 
                                        "framerate", GST_TYPE_FRACTION, 30, 1, 
                                        NULL);
    
    g_object_set(G_OBJECT(src_), "do-timestamp", true, NULL);
    g_object_set(G_OBJECT(decoder_), "mjpeg", 1, NULL);
    g_object_set(G_OBJECT(capsfilter_), "caps", caps, NULL);
    g_object_set(G_OBJECT(decoder_), "enable-max-performance", true, NULL);

    gst_bin_add_many(GST_BIN(bin_), src_, converter_, decoder_, capsfilter_, NULL);

    if (!gst_element_link_many(src_, capsfilter_, decoder_, converter_, NULL)) {
        g_warning ("Failed to link element1 and element2!");
    }
    gst_caps_unref (caps);
}

GstElement* WebCamInput::get_bin(){
    return bin_;
}

const std::string WebCamInput::get_source() const {
    char source[40];
    g_object_get(G_OBJECT(src_), "device", &source, NULL);
    return std::string(source);
}

void WebCamInput::set_source(const std::string& source) {
    g_object_set(G_OBJECT(src_), "device", source.c_str(), "do-timestamp", true, NULL);
    gst_element_add_pad(bin_, gst_ghost_pad_new("src", gst_element_get_static_pad(converter_, "src")));   
}
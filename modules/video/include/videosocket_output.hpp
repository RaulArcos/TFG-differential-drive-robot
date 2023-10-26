#ifndef VIDEOSOCKET_OUTPUT_HPP_
#define VIDEOSOCKET_OUTPUT_HPP_

#include "common.hpp"
#include <gst/gst.h>

namespace robotuca{
    class VideoSocketOutput{
        public:
            VideoSocketOutput(const Resolution& res);
            ~VideoSocketOutput() = default;

            GstElement* get_bin();
        private:
            GstElement* bin_;
            GstElement* sink_;
            GstElement* capsfilter_;
    };
}

#endif
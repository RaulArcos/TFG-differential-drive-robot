#ifndef WEBCAM_INPUT_HPP_
#define WEBCAM_INPUT_HPP_

#include "common.hpp"
#include <gst/gst.h>
#include <string>

namespace robotuca{
    class WebCamInput{
        public:
            WebCamInput(const Resolution& res);
            ~WebCamInput() = default;

            GstElement* get_bin();

            const std::string get_source() const;
            void set_source(const std::string& source);
        private:
            GstElement* bin_;
            GstElement* src_;
            GstElement* converter_;
            GstElement* decoder_;
            GstElement* queue_;
            GstElement* capsfilter_;
    };
}

#endif
#!/usr/bin/sh
export LD_PRELOAD=/usr/lib64/libv4l/v4l2convert.so
zoom "$@"

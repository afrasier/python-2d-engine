#!/bin/bash

# Creates a virtual frame buffer to make tests run faster
Xvfb :1 -screen 0 1920x1080x24&
DISPLAY=:1 pytest
killall Xvfb

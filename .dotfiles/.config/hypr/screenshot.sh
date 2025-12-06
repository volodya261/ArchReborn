#!/bin/bash

temp_screenshot="/tmp/screenshot.png"
save_file=$(date +'%y%m%d_%Hh%Mm%Ss_screenshot.png')

grim -g "$(slurp)" - | wl-copy && wl-paste > $temp_screenshot | dunstify "Screenshot of the region taken" -t 1000 && swappy -f $temp_screenshot

rm "$temp_screenshot"




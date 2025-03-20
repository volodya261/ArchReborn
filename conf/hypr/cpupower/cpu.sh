#!/bin/bash
for cpu in /sys/devices/system/cpu/cpu[0-9]*/cpufreq/scaling_cur_freq; do
    freq=$(cat $cpu)
    echo "$(basename $(dirname $cpu)): $((freq / 1000)) MHz"
done


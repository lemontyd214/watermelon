#!/bin/bash
while [ 1 ]; do
    python3 dota2_download.py
    if [ $? == 0 ]; then
        rsync -av --exclude='*.log' /root/youtube 1.117.160.182:/root
    fi
    sleep 300
done

#!/bin/bash
while [ 1 ]; do
    python3 dota2_upload.py
    if [ $? == 0 ]; then
        rsync -av --exclude='*.log' /root/youtube 43.129.219.16:/root
    fi
    sleep 300
done
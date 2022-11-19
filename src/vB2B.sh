#!/bin/bash

Service()
{
    cp -rf ../f_satatic/* / 2>/dev/null

    systemctl daemon-reload
    systemctl disable vB2B.service
    systemctl enable vB2B.service

    systemctl stop vB2B.service
    systemctl start vB2B.service

    systemctl status vB2B.service
    systemctl show vB2B.service

}

Log() 
{
    local aMsg="$1";

    Msg="$(date +%Y-%m-%d-%a), $(date +%H:%M:%S), $(id -u -n), $(whoami) $aMsg"
    echo "$Msg"
    #echo "$Msg"  >> $0.log
    echo "$Msg"  >> /tmp/vB2B.log
}

Log "PWD: $(pwd)"
#cd $(dirname $0)

#env python3 -V
#/usr/bin/env python -B vB2B.py -s
#/home/vladvons/VirtEnv/python3.10/bin/python3 -B vB2B.py -s
python3 -V
/home/vladvons/VirtEnv/python3.10/bin/python3 -B vB2B.py -s

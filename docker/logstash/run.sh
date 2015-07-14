#!/bin/bash

/etc/init.d/logstash start

/usr/bin/tail -f /dev/null
sleep 10s

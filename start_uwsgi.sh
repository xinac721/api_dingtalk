#!/bin/sh

uwsgi --ini /data/wwwroot/xinac_api/uwsgi.ini -d /var/log/uwsgi.log

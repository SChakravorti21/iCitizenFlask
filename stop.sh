#! /bin/bash


kill -9 `ps -aef | grep 'celery_worker_bills' | grep -v grep | awk '{print $2}'`
sleep 1
kill -9 `ps -aef | grep 'celery_worker_events' | grep -v grep | awk '{print $2}'`
sleep 1
kill -9 `ps -aef | grep 'celery_worker_polls' | grep -v grep | awk '{print $2}'`
sleep 1
kill -9 `ps -aef | grep 'python3 run.py' | grep -v grep | awk '{print $2}'`
sleep 1
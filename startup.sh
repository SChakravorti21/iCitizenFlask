#! /bin/bash


kill -9 `ps -aef | grep 'celery_worker_bills' | grep -v grep | awk '{print $2}'`
sleep 1
kill -9 `ps -aef | grep 'celery_worker_events' | grep -v grep | awk '{print $2}'`
sleep 1
kill -9 `ps -aef | grep 'celery_worker_polls' | grep -v grep | awk '{print $2}'`
sleep 1
kill -9 `ps -aef | grep 'python3 run.py' | grep -v grep | awk '{print $2}'`
sleep 1

mkdir -p ~/log
source venv/bin/activate
export ICITIZEN_MONGODB_URI=mongodb://iCitizen:icitizenapp1@ds135747.mlab.com:35747/icitizen

celery -A celery_app.celery_worker_bills worker -n "bill" --loglevel=info > ~/log/bills_out.txt 2>&1 &
celery -A celery_app.celery_worker_events worker -n "events" --loglevel=info > ~/log/events_out.txt 2>&1 &
celery -A celery_app.celery_worker_polls worker -n "polls" --loglevel=info > ~/log/polls_out.txt 2>&1 &

python3 run.py > ~/log/main_out.txt 2>&1 &
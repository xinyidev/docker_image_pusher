#!/bin/sh

echo "***********************************"
echo "start ddddocr"

if netstat -an | grep "10020" | grep -i listen >/dev/null ; then
  #kill -9 $(lsof -i tcp:10020)
  echo "ddddocr is running."
else
  echo "ddddocr is starting."
  exec gunicorn -k gevent -w 2 -b 0.0.0.0:10020 app:app
fi
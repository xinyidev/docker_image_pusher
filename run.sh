#!/bin/sh

echo "***********************************"
echo "start ddddocr"

if netstat -an | grep "10022" | grep -i listen >/dev/null ; then
  #kill -9 $(lsof -i tcp:10020)
  echo "PaddleOCR is running."
else
  echo "PaddleOCR is starting."
  exec gunicorn -k gevent -w 2 -b 0.0.0.0:10022 app:app
fi
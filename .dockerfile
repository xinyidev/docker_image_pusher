FROM python:3.11-slim-bookworm AS base
MAINTAINER xinyi "xinyigao@zego.im"
WORKDIR /home/workspace

COPY ./app.py /home/workspace/app.py
COPY ./run.sh /home/workspace/run.sh

RUN chmod u+x /home/workspace/run.sh

RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip3 install --upgrade pip setuptools flask && \
    pip install ddddocr && \
    pip install gunicorn && pip install gevent

RUN sed -i s@/archive.ubuntu.com/@/mirrors.ustc.edu.cn/@g /etc/apt/sources.list.d/debian.sources \
    && sed -i s@/deb.debian.org/@/mirrors.ustc.edu.cn/@g /etc/apt/sources.list.d/debian.sources \
    && apt-get clean -y \
    && apt-get autoclean -y \
    && apt-get update -y \
    && apt-get install net-tools -y && apt-get install curl -y

RUN cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && echo "Asia/Shanghai" > /etc/timezone

ENTRYPOINT ["/bin/sh","-c","/home/workspace/run.sh"]
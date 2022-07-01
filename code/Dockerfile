# (c) Copyright 2019-2022, James Stevens ... see LICENSE for details

FROM alpine:3.16

RUN rmdir /tmp
RUN ln -s /dev/shm /tmp
RUN ln -s /dev/shm /ram

RUN apk add nginx
RUN apk add python3 py3-gunicorn py3-flask 
RUN apk add py3-dnspython py3-requests

RUN rmdir /var/lib/nginx/tmp /var/log/nginx
RUN ln -s /dev/shm /var/lib/nginx/tmp
RUN ln -s /dev/shm /var/log/nginx
RUN ln -s /dev/shm /ram/nginx

RUN addgroup nginx daemon

COPY etc/nginx.conf /etc/nginx/nginx.conf
COPY etc/crontab /etc/crontabs/root
COPY etc/inittab /etc/inittab
COPY etc /usr/local/etc/

COPY wallet /usr/local/wallet
RUN python3 -m compileall /usr/local/wallet

COPY bin /usr/local/bin/
COPY htdocs /opt/htdocs/

CMD [ "/sbin/init" ]

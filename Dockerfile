FROM python:3.8-alpine

WORKDIR /src/

ADD storyteller /src/
RUN \
  adduser -D flask && \
  #apk add --no-cache tar py3-cryptography py3-pillow aws-cli bash libc6-compat && \
  apk add --no-cache py3-cryptography py3-pillow aws-cli libc6-compat && \
  wget -O daemon.zip https://s3.dualstack.us-east-2.amazonaws.com/aws-xray-assets.us-east-2/xray-daemon/aws-xray-daemon-linux-3.x.zip && \
  unzip daemon.zip && \
  mv -v xray /usr/bin/xray && \
  chown -R flask:flask /src/* /usr/bin/xray && \
  chmod -v 0777 /usr/bin/xray && \
  rm daemon.zip cfg.yaml && \
  #wget https://dl.influxdata.com/telegraf/releases/telegraf-1.15.3_linux_amd64.tar.gz && \
  #tar xfv telegraf-1.15.3_linux_amd64.tar.gz && \
  #mv ./telegraf-1.15.3/usr/lib/telegraf/scripts/init.sh /etc/rc.d/ && \
  #rm -rf telegraf* && \
  pip install --no-compile --no-cache-dir -r /src/requirements.txt && \
  chmod +x /src/boot.sh

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED TRUE

USER flask

EXPOSE 5000
ENTRYPOINT ["/src/boot.sh"]

FROM python:3.8-alpine

WORKDIR /src/

ADD storyteller /src/
RUN \
  wget -O daemon.zip https://s3.dualstack.us-east-2.amazonaws.com/aws-xray-assets.us-east-2/xray-daemon/aws-xray-daemon-linux-3.x.zip && \
  unzip daemon.zip && \
  mv -v xray /usr/bin/xray && \
  rm daemon.zip cfg.yaml && \
  pip install --no-compile --no-cache-dir -r /src/requirements.txt && \
  chmod +x /src/boot.sh && \
  adduser -D flask && \
  chown -R flask:flask /src/* /usr/bin/xray && \
  chmod -v 0777 /usr/bin/xray && \
  apk add --no-cache py3-pillow aws-cli bash libc6-compat

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED TRUE

USER flask

EXPOSE 5000
ENTRYPOINT ["/src/boot.sh"]

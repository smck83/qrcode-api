FROM pypy:3.9
LABEL maintainer="s@mck.la"
ARG MY_APP_PATH=/opt/generate-qr-code

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    ntp \
    && mkdir -p ${MY_APP_PATH}

ADD main.py requirements.txt run.py ${MY_APP_PATH}
RUN pip3 install -r ${MY_APP_PATH}/requirements.txt
#RUN pip3 install fastapi uvicorn[standard] qrcode[pil] requests
WORKDIR ${MY_APP_PATH}


VOLUME [${MY_APP_PATH}]

ENTRYPOINT pypy3 -u run.py

EXPOSE 8000/tcp

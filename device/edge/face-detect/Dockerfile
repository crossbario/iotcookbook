FROM crossbario/autobahn-python:cpy3

USER root

WORKDIR /workspace

RUN    apt update \
    && apt install unzip libsm6 libxext6 libxrender1 -y \
    && wget https://github.com/crossbario/iotcookbook/archive/master.zip \
    && unzip master.zip \
    && pip3 install -r iotcookbook-master/device/edge/face-detect/app/requirements.txt \
    && apt clean \
    && rm -rf ~/.cache/pip \
    && rm -rf /var/lib/apt/lists/

WORKDIR /workspace/iotcookbook-master/device/edge/face-detect/app/

CMD ["python3", "-u", "server.py"]

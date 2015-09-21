FROM python:2.7

ENV INSTANCE=docker

# Chinese Localisation
ENV CHINESE_LOCAL_PIP_CONFIG="--index-url http://pypi.douban.com/simple --trusted-host pypi.douban.com"

COPY ./requirements.txt /tmp/
RUN pip install --requirement /tmp/requirements.txt ${CHINESE_LOCAL_PIP_CONFIG}

WORKDIR '/rhizome'

FROM python:2.7

ENV INSTANCE=docker

# Download and install wkhtmltopdf
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install sudo
RUN apt-get install xvfb
RUN sudo apt-get install -y wkhtmltopdf


# Chinese Localisation
ENV CHINESE_LOCAL_PIP_CONFIG="--index-url http://pypi.douban.com/simple --trusted-host pypi.douban.com"

COPY ./requirements.txt /tmp/
RUN pip install --requirement /tmp/requirements.txt ${CHINESE_LOCAL_PIP_CONFIG}

WORKDIR '/rhizome'

FROM python:2.7

ENV POSTGRES_VERSION=9.3
ENV DB_USER=djangoapp
ENV DB_PWD=w3b@p01i0

# Chinese Localisation
ENV CHINESE_LOCAL_PIP_CONFIG="--index-url http://pypi.douban.com/simple --trusted-host pypi.douban.com"

RUN wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -
RUN echo "deb http://apt.postgresql.org/pub/repos/apt/ precise-pgdg main" > /etc/apt/sources.list.d/pgdg.list

RUN apt-get update
RUN apt-get install -y \
  postgresql-${POSTGRES_VERSION} \
  postgresql-client-${POSTGRES_VERSION} \
  postgresql-contrib-${POSTGRES_VERSION}

USER root
COPY ./requirements.txt /tmp/
RUN pip install --requirement /tmp/requirements.txt ${CHINESE_LOCAL_PIP_CONFIG}

RUN echo "host all  all    0.0.0.0/0  md5" >> /etc/postgresql/${POSTGRES_VERSION}/main/pg_hba.conf
RUN echo "listen_addresses='*'" >> /etc/postgresql/${POSTGRES_VERSION}/main/postgresql.conf

EXPOSE 5432

USER postgres
RUN /etc/init.d/postgresql start && \
  createuser --no-createdb --no-createrole --no-superuser djangoapp && \
  psql -c "ALTER USER ${DB_USER} WITH PASSWORD '${DB_PWD}';" && \
  createuser --no-createdb --no-createrole --no-superuser root && \
  psql -c "ALTER USER root WITH PASSWORD 'root';" && \
  createdb polio --owner ${DB_USER} --encoding=utf8 --template template0 && \
  createdb rhizome --owner ${DB_USER} --encoding=utf8 --template template0

WORKDIR '/etc/polio'
USER root
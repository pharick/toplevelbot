FROM postgres:11

RUN mkdir -p /docker-entrypoint-initdb.d
COPY ./add_hstore.sh /docker-entrypoint-initdb.d/add_hstore.sh
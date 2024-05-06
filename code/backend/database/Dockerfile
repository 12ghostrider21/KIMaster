FROM postgres

WORKDIR /app

COPY init.sql /docker-entrypoint-initdb.d/

EXPOSE 5432

ENV POSTGRES_USER dbuser
ENV POSTGRES_PASSWORD dbpassword
ENV POSTGRES_DB clientdb

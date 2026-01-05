FROM python:3.12.3-bullseye
LABEL org.opencontainers.image.authors="murat.kendir@tum.de"
LABEL maintainer="murat.kendir@tum.de"
LABEL composition=citydb-3dtiler

RUN useradd --home-dir /home/tester --create-home --shell /bin/bash tester
RUN usermod --append --groups root tester

WORKDIR /home/tester/citydb-3dtiler
COPY . .

RUN chown -R tester /home/tester

RUN apt-get update && \
    apt-get install -y curl gnupg2 lsb-release && \
    echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list && \
    curl -fsSL https://www.postgresql.org/media/keys/ACCC4CF8.asc | gpg --dearmor -o /etc/apt/trusted.gpg.d/postgresql.gpg && \
    apt-get update && \
    apt-get install -y postgresql-client

# Donwload and unzip pg23dm version 2.25.0

RUN wget --directory-prefix /home/tester/downloads --quiet https://github.com/Geodan/pg2b3dm/releases/download/v2.25.0/pg2b3dm-linux-x64.zip

RUN unzip -d /home/tester/citydb-3dtiler/tiler_app /home/tester/downloads/pg2b3dm-linux-x64.zip

RUN rm /home/tester/downloads/pg2b3dm-linux-x64.zip

ENV PIP_ROOT_USER_ACTION=ignore

RUN pip install --upgrade pip
RUN pip install --force-reinstall -v "psycopg2-binary==2.9.11"
RUN pip install --force-reinstall -v "PyYAML==6.0.3"

ENTRYPOINT ["python3", "./citydb-3dtiler.py"]
CMD ["--help", "advise", "tile"]

USER tester
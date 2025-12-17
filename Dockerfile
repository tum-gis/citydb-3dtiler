FROM python:3.12.3-bullseye
LABEL org.opencontainers.image.authors="murat.kendir@tum.de"
LABEL maintainer="murat.kendir@tum.de"
LABEL composition=citydb-3dtiler

RUN useradd --home-dir /home/tester --create-home --shell /bin/bash tester
RUN usermod --append --groups root tester

WORKDIR /home/tester/citydb-3dtiler
COPY . .

RUN chown -R tester /home/tester

ENV PIP_ROOT_USER_ACTION=ignore

RUN pip install --upgrade pip
RUN pip install --force-reinstall -v "psycopg2-binary==2.9.11"
RUN pip install --force-reinstall -v "PyYAML==6.0.3"

ENTRYPOINT ["python3", "./citydb-3dtiler.py"]
CMD ["--help", "advise", "tile"]

USER tester
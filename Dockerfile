FROM python:3.12.3-bullseye
LABEL org.opencontainers.image.authors="murat.kendir@tum.de"
LABEL maintainer="murat.kendir@tum.de"
LABEL composition=citydb-3dtiler

WORKDIR /home/citydb-3dtiler
COPY . .

ENV PIP_ROOT_USER_ACTION=ignore

RUN pip install --upgrade pip
RUN pip install --force-reinstall -v "psycopg2-binary==2.9.11"
RUN pip install --force-reinstall -v "PyYAML==6.0.3"

ENTRYPOINT ["python3", "./citydb-3dtiler.py"]
CMD ["--help", "advise", "tile"]

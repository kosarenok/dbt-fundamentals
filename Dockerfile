FROM apache/airflow:slim-2.10.5-python3.11

ENV TZ="Europe/Moscow"

USER root

RUN apt-get update && apt-get install -y --no-install-recommends \
    make \
    postgresql-client \
    tzdata \
    && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime \
    && echo $TZ > /etc/timezone \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN if getent group airflow; then groupmod -g 1000 airflow; else groupadd -g 1000 airflow; fi && \
    usermod -u 1000 -g 1000 airflow && \
    chown -R airflow:airflow /opt/airflow

WORKDIR /opt/airflow

# Copy requirements first to leverage Docker cache
COPY --chown=airflow:airflow requirements.txt .

USER airflow

RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=airflow:airflow . .

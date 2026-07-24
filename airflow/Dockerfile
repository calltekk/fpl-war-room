FROM apache/airflow:3.3.0-python3.12

USER root

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        curl \
        git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN mkdir -p /opt/fpl-venv /tmp/fpl-dependencies \
    && chown -R airflow:root \
        /opt/fpl-venv \
        /tmp/fpl-dependencies

COPY --chown=airflow:root \
    pyproject.toml \
    uv.lock \
    /tmp/fpl-dependencies/

USER airflow

RUN cd /tmp/fpl-dependencies \
    && UV_PROJECT_ENVIRONMENT=/opt/fpl-venv \
       uv sync \
       --frozen \
       --no-dev \
       --no-install-project

RUN uv pip install \
    --python /opt/fpl-venv/bin/python \
    "dbt-core==1.12.0" \
    "dbt-postgres==1.11.0"

ENV PATH="/opt/fpl-venv/bin:${PATH}"

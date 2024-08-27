ARG BASE_IMAGE=python:3.10.14
ARG CODE_LOCATION_NAME=dagster_project
# Build stage 1: Installing depedencies with Poetry
FROM ${BASE_IMAGE} as builder

RUN pip install poetry==1.8.3

WORKDIR /app

COPY pyproject.toml ./
RUN poetry config virtualenvs.create true
RUN poetry config virtualenvs.in-project true
RUN poetry install --only main --no-root --no-interaction

# Build stage 2: Runtime code for codeserver
FROM ${BASE_IMAGE} as codeserver

# Copy venv from builder
ENV VIRTUAL_ENV=/app/.venv
COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

# Add repository code
ARG APP_DIR=/opt/dagster/app
WORKDIR ${APP_DIR}

# Copy only the things we need
COPY ${CODE_LOCATION_NAME} ${APP_DIR}/${CODE_LOCATION_NAME}

ENV PATH=${VIRTUAL_ENV}/bin:$PATH
ENV PYTHONPATH=${APP_DIR}

# Run dagster gRPC server on port 4000
EXPOSE 4000

CMD ["dagster", "api", "grpc", "-h", "0.0.0.0", "-p", "4000", "-m", "dagster_project"]
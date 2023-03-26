FROM python:3.9 as base

WORKDIR /pipelines
RUN pip install --upgrade pip

ENV POETRY_VERSION=1.4.1
ENV POETRY_HOME=/opt/poetry
ENV POETRY_BIN=$POETRY_HOME/bin/poetry

# Create stage for Poetry installation
FROM base as dep-poetry

# Creating a virtual environment just for poetry and install it with pip
RUN python3 -m venv $POETRY_HOME \
    && $POETRY_HOME/bin/pip install poetry==${POETRY_VERSION}

# Copy Dependencies
COPY poetry.lock pyproject.toml ./

# Install Dependencies
RUN $POETRY_BIN config --local virtualenvs.create false
RUN $POETRY_BIN install --no-root

# Copy Application
COPY ./db /pipelines/db
COPY ./example_pipeline/original /pipelines/example_pipeline/original
COPY ./pipeline.py /pipelines/
COPY ./pipelines /pipelines/pipelines
COPY ./README.md /pipelines
RUN pip install .

# Run Application
CMD ["python", "./pipeline.py"]

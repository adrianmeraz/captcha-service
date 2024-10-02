FROM public.ecr.aws/lambda/python:3.12

ENV POETRY_VERSION=1.8.3

# Install Poetry
RUN pip install "poetry==$POETRY_VERSION"

# Copy only requirements to cache them in docker layer
WORKDIR ${LAMBDA_TASK_ROOT}
COPY poetry.lock pyproject.toml ${LAMBDA_TASK_ROOT}/

# Project initialization: (Now using --without dev as replacement for --no-dev per https://python-poetry.org/docs/cli/
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi --no-root --only main

# Copy app to Docker Image
COPY src ${LAMBDA_TASK_ROOT}/src

# View what was added to image
RUN ls -R

# Test the image
CMD [ "src.lambdas.event_handler.lambda_handler" ]

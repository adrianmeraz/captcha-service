# For further details on why AWS base images are used, see: https://aws.amazon.com/blogs/compute/optimizing-lambda-functions-packaged-as-container-images/
FROM public.ecr.aws/lambda/python:3.12

ENV POETRY_VERSION=1.8.3
WORKDIR ${LAMBDA_TASK_ROOT}
CMD [ "src.lambdas.event_handler.lambda_handler" ]

# Install Poetry
RUN pip install "poetry==$POETRY_VERSION"

# Cache dependencies
COPY poetry.lock pyproject.toml ${LAMBDA_TASK_ROOT}/

# Install Dependencies, and view what was added to image
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi --no-root --no-dev

# Copy app to Docker Image
COPY src ${LAMBDA_TASK_ROOT}/src

# View Directory Contents
RUN ls -R
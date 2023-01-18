FROM python:3.8.10 as base

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1
ENV PYTHONUNBUFFERED 1

RUN python -m pip install --upgrade pip
#RUN pip install poetry
#RUN poetry install

ENV POETRY_VERSION=1.2.2
ENV POETRY_HOME='/opt/poetry'
ENV POETRY_VENV='/opt/poetry-venv'
ENV POETRY_CACHE_DIR='/opt/.cache'
ENV PYTHONPATH="${PYTHONPATH}:/app-workspace"

WORKDIR /app-workspace
COPY . .

RUN python -m venv $POETRY_VENV \
    && $POETRY_VENV/bin/pip install -U pip setuptools \
    && $POETRY_VENV/bin/pip install poetry==${POETRY_VERSION}

ENV PATH="$POETRY_VENV/bin:$PATH"

RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-ansi

RUN pip3 install torch torchvision --extra-index-url https://download.pytorch.org/whl/cpu

CMD ["poetry", "run", "python", "./emotion_model/model.py", "--name", "emotion_model","--type","emotion"]

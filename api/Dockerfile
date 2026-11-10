FROM python:3.12.16-slim AS build

ENV PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

RUN python -m venv /venv
COPY requirements.txt .
RUN /venv/bin/pip install -r requirements.txt \
    && /venv/bin/pip uninstall -y pip

FROM python:3.12.16-slim

ENV PATH=/venv/bin:$PATH \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN python -m pip uninstall -y --root-user-action=ignore pip \
    && useradd --system --uid 10001 --no-create-home api

COPY --from=build /venv /venv
WORKDIR /srv
COPY app/ app/

USER api
EXPOSE 8000
CMD ["uvicorn", "app.main:create_app", "--factory", "--host", "0.0.0.0", "--port", "8000"]

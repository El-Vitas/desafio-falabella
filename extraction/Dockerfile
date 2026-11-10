FROM python:3.12.16-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DATA_DIR=/data

WORKDIR /app

COPY extraction/requirements.txt extraction/requirements.txt
RUN pip install --no-cache-dir --root-user-action=ignore -r extraction/requirements.txt \
    && pip uninstall -y --root-user-action=ignore pip

COPY extraction/ extraction/
COPY generator/ generator/

CMD ["sh", "extraction/entrypoint.sh"]

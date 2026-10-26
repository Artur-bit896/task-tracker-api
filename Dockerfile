
FROM python:3.12-slim

WORKDIR /app


#чтобы у всех не было крутых привилегий
RUN useradd --create-home appuser

RUN pip install uv

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-dev

COPY app ./app
COPY alembic ./alembic
COPY alembic.ini ./

CMD ["uv", "run", "--no-sync", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

#делаем юзера
USER appuser
FROM python:3.13-alpine

WORKDIR /loft

COPY pyproject.toml .
RUN pip install --no-cache-dir .

COPY . .

ENTRYPOINT ["python", "-m", "loft"]

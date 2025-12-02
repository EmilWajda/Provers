FROM python:3.13-alpine

RUN apk add --no-cache docker-cli docker-cli-compose

WORKDIR /loft

COPY pyproject.toml .
RUN pip install --no-cache-dir .

COPY . .

ENTRYPOINT ["python", "-m", "loft"]

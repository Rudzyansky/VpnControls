FROM python:3.10-alpine

RUN apk add --no-cache strongswan pwgen tzdata && \
    ln -sf /usr/share/zoneinfo/Europe/Moscow /etc/localtime && echo "Europe/Moscow" > /etc/timezone

COPY requirements.txt /
RUN pip install --no-cache-dir --disable-pip-version-check -r /requirements.txt

WORKDIR /app
ADD . .

CMD ["python", "-m", "main"]

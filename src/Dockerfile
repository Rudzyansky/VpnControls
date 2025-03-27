FROM python:3.10-alpine AS base

# Timezone
RUN apk add --no-cache tzdata && \
    ln -sf /usr/share/zoneinfo/Europe/Moscow /etc/localtime && \
    echo "Europe/Moscow" > /etc/timezone

# Pwgen
RUN apk add --no-cache pwgen

COPY requirements.txt /
RUN pip install --no-cache-dir --disable-pip-version-check -r /requirements.txt

WORKDIR /app
ADD . .

ENTRYPOINT ["python", "-m"]
CMD ["main"]

FROM python:3.10-alpine AS base

# Timezone
RUN apk add --no-cache tzdata && \
    ln -sf /usr/share/zoneinfo/Europe/Moscow /etc/localtime && \
    echo "Europe/Moscow" > /etc/timezone

# Pwgen
RUN apk add --no-cache pwgen

COPY requirements.txt /
RUN pip install --no-cache-dir --disable-pip-version-check -r /requirements.txt

# Cleanup
RUN rm -rf  \
    /usr/lib/python3/dist-packages/pip-*.dist-info \
    /usr/lib/python3/dist-packages/setuptools-*.egg-info \
    /usr/lib/python3/dist-packages/wheel-*.egg-info

WORKDIR /app
ADD . .

ENTRYPOINT ["python", "-m"]
CMD ["main"]

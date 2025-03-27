FROM python:3.10-slim

RUN apt-get -qq update && apt-get -qq install --no-install-recommends pwgen tzdata && \
    ln -sf /usr/share/zoneinfo/Europe/Moscow /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata

COPY requirements.txt /
RUN pip install --no-cache-dir --disable-pip-version-check -r /requirements.txt

WORKDIR /app
ADD . .

CMD ["python", "-m", "main"]

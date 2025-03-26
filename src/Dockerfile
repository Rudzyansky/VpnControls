FROM python:3.10-slim AS base

# Timezone
RUN apt-get -qq update && apt-get -qq install --no-install-recommends tzdata && \
    ln -sf /usr/share/zoneinfo/Europe/Moscow /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata

# Pwgen
RUN apt-get -qq update && apt-get -qq install --no-install-recommends pwgen

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

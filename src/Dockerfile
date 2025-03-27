FROM python:3.10-alpine AS base

# --- Install dependencies and download sgerrand’s key ---
RUN apk add --no-cache --virtual .build-deps wget ca-certificates \
 && update-ca-certificates \
 && wget -q -O /etc/apk/keys/sgerrand.rsa.pub https://alpine-pkgs.sgerrand.com/sgerrand.rsa.pub

# --- Install glibc from sgerrand’s releases ---
#   • Check https://github.com/sgerrand/alpine-pkg-glibc/releases
#     for the latest version number (e.g., 2.35-r0 or later).
#
#   Example below uses 2.35-r0. Replace to the exact version you want.
RUN GLIBC_VERSION="2.35-r1" \
 && wget -q "https://github.com/sgerrand/alpine-pkg-glibc/releases/download/${GLIBC_VERSION}/glibc-${GLIBC_VERSION}.apk" \
 && apk add --no-cache "glibc-${GLIBC_VERSION}.apk" \
 && rm "glibc-${GLIBC_VERSION}.apk"

# --- (Optional) Clean up .build-deps if you don’t need them anymore ---
RUN apk del .build-deps

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

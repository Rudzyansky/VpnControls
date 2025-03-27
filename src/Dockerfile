FROM alpine:latest AS glibc-builder
ARG TARGETARCH
ARG GLIBC_VERSION=2.41

RUN apk add --no-cache \
    build-base \
    bash \
    coreutils \
    binutils \
    linux-headers \
    bison \
    gawk \
    texinfo \
    curl \
    patch

WORKDIR /tmp
RUN curl https://ftp.gnu.org/gnu/glibc/glibc-${GLIBC_VERSION}.tar.gz -o glibc-${GLIBC_VERSION}.tar.gz && \
    tar -xf glibc-${GLIBC_VERSION}.tar.gz

WORKDIR /tmp/glibc-${GLIBC_VERSION}
RUN mkdir build

RUN set -eux; \
    if [ "${TARGETARCH}" = "amd64" ]; then \
      GLIBC_HOST="x86_64-unknown-linux-gnu"; \
      GLIBC_BUILD="x86_64-unknown-linux-musl"; \
      LD_SO="ld-linux-x86-64.so.2"; \
    elif [ "${TARGETARCH}" = "arm64" ]; then \
      GLIBC_HOST="aarch64-unknown-linux-gnu"; \
      GLIBC_BUILD="aarch64-unknown-linux-musl"; \
      LD_SO="ld-linux-aarch64.so.1"; \
    else \
      echo "Unsupported architecture: ${TARGETARCH}"; \
      exit 1; \
    fi; \
    cd build; \
    ../configure \
      --prefix=/usr/glibc-compat \
      --host="${GLIBC_HOST}" \
      --build="${GLIBC_BUILD}" \
      --enable-obsolete-rpc \
      --enable-kernel=3.7.0; \
    make -j"$(nproc)"; \
    make install DESTDIR=/tmp/glibc-staging


FROM python:3.10-alpine
ARG TARGETARCH
ARG GLIBC_VERSION=2.36

COPY --from=glibc-builder /tmp/glibc-staging/ /
RUN set -eux; \
    if [ "${TARGETARCH}" = "amd64" ]; then \
      export LD_SO="ld-linux-x86_64.so.1"; \
    elif [ "${TARGETARCH}" = "arm64" ]; then \
      export LD_SO="ld-linux-aarch64.so.1"; \
    else \
      echo "Unsupported architecture: ${TARGETARCH}"; \
      exit 1; \
    fi; \
    ln -s "/usr/glibc-compat/lib/${LD_SO}" "/lib/${LD_SO}"; \
    echo "Successfully symlinked loader for ${TARGETARCH}."

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

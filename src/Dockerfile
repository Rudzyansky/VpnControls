FROM alpine:latest AS glibc-builder

ARG TARGETARCH
ARG GLIBC_VERSION=2.41

RUN apk add --no-cache build-base bash coreutils binutils linux-headers bison gawk texinfo curl patch python3

WORKDIR /tmp

# Download & unpack glibc sources
RUN curl -sSL "https://ftp.gnu.org/gnu/glibc/glibc-${GLIBC_VERSION}.tar.gz" -o glibc.tar.gz && tar -xf glibc.tar.gz

WORKDIR /tmp/glibc-${GLIBC_VERSION}
RUN mkdir build
WORKDIR /tmp/glibc-${GLIBC_VERSION}/build

RUN set -eux; \
    ../configure \
      --prefix=/usr/glibc-compat \
      --enable-obsolete-rpc \
      --enable-kernel=3.7.0 \
      --disable-werror; \
    make -j"$(nproc)"; \
    make install DESTDIR=/tmp/glibc-staging


FROM python:3.10-alpine

ARG TARGETARCH
ARG GLIBC_VERSION=2.41

# Copy the glibc artifacts from builder
COPY --from=glibc-builder /tmp/glibc-staging/ /

# Symlink the correct loader for each architecture
RUN set -eux; \
    if [ "${TARGETARCH}" = "amd64" ]; then ln -s /usr/glibc-compat/lib/ld-linux-x86-64.so.2 /lib/ld-linux-x86-64.so.2; \
    elif [ "${TARGETARCH}" = "arm64" ]; then ln -s /usr/glibc-compat/lib/ld-linux-aarch64.so.1 /lib/ld-linux-aarch64.so.1; \
    else echo "Unsupported architecture: ${TARGETARCH}"; exit 1; fi

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

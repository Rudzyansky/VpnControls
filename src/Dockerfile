###
# Stage 1: glibc-builder on Debian (glibc-based)
###
FROM --platform=$BUILDPLATFORM debian:stable AS glibc-builder

ARG TARGETARCH
ARG GLIBC_VERSION=2.41

# Install build deps (Debian's toolchain is glibc-based)
RUN apt-get -qq update && apt-get -qq install -y \
    build-essential \
    bash \
    binutils \
    linux-libc-dev \
    bison \
    gawk \
    texinfo \
    curl \
    patch \
    python3 \
    wget

WORKDIR /tmp

# Download glibc sources
RUN wget -q "https://ftp.gnu.org/gnu/glibc/glibc-${GLIBC_VERSION}.tar.gz" -O glibc.tar.gz && tar -xf glibc.tar.gz

WORKDIR /tmp/glibc-${GLIBC_VERSION}
RUN mkdir build
WORKDIR /tmp/glibc-${GLIBC_VERSION}/build

# Configure & build glibc natively (Debian environment is glibc-based, so no cross trouble)
RUN set -eux; \
    ../configure \
      --prefix=/usr/glibc-compat \
      --enable-obsolete-rpc \
      --enable-kernel=3.7.0 \
      --disable-werror; \
    make -j"$(nproc)"; \
    make install DESTDIR=/tmp/glibc-staging


###
# Stage 2: final Alpine-based image
###
FROM --platform=$TARGETARCH python:3.10-alpine

ARG TARGETARCH
ARG GLIBC_VERSION=2.41

# Copy glibc from the Debian builder
COPY --from=glibc-builder /tmp/glibc-staging/ /

# Symlink the loader for each architecture
RUN set -eux; \
    if [ "${TARGETARCH}" = "amd64" ]; then \
      ln -s /usr/glibc-compat/lib/ld-linux-x86-64.so.2 /lib/ld-linux-x86-64.so.2; \
    elif [ "${TARGETARCH}" = "arm64" ]; then \
      ln -s /usr/glibc-compat/lib/ld-linux-aarch64.so.1 /lib/ld-linux-aarch64.so.1; \
    else \
      echo "Unsupported arch: ${TARGETARCH}"; \
      exit 1; \
    fi

RUN apk add --no-cache pwgen tzdata && \
    ln -sf /usr/share/zoneinfo/Europe/Moscow /etc/localtime && echo "Europe/Moscow" > /etc/timezone

COPY requirements.txt /
RUN pip install --no-cache-dir --disable-pip-version-check -r /requirements.txt

WORKDIR /app
ADD . .

ENTRYPOINT ["python", "-m"]
CMD ["main"]

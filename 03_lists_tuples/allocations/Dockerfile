FROM ubuntu:24.04

RUN apt update && apt upgrade -y && \
    apt install -y \
        build-essential \
        git \
        zlib1g-dev \
        libffi-dev \
        libreadline-dev \
        libncursesw5-dev \
        libssl-dev \
        libsqlite3-dev \
        libgdbm-dev \
        libc6-dev \
        libbz2-dev \
        && \
    apt autoremove -y && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /build
RUN git clone -b 3.12-hppv3 https://github.com/mynameisfiber/cpython.git && \
    cd cpython && \
    ./configure && \
    make -j && \
    make install

RUN python3 -m ensurepip

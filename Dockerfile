ARG HUGO_VERSION=0.111.3
ARG DIST_TAG=-ext-ubuntu
FROM klakegg/hugo:${HUGO_VERSION}${DIST_TAG}

ARG DOCSY_VERSION=v0.7.1

LABEL maintainer="CoMSES Net <support@comses.net>"

WORKDIR /src
COPY config.toml package.json /src/

RUN git config --global --add safe.directory /src \
    && hugo mod init github.com/openmodelingfoundation/openmodelingfoundation.github.io \
    && hugo mod get github.com/google/docsy@${DOCSY_VERSION}

COPY . /src/

CMD ["server"]

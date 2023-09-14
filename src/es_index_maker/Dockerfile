FROM alpine:latest

WORKDIR /opt/elastic_filler

RUN apk add curl
COPY . .

ENTRYPOINT [ "sh", "entrypoint.sh" ]
FROM mcr.microsoft.com/devcontainers/universal:2

# Install Redis 6 and RediSearch
RUN apt-get update && apt-get install -y software-properties-common && \
    add-apt-repository ppa:redislabs/redis && \
    apt-get update && \
    apt-get install -y redis-server redisearch-module

# Any other setup you need

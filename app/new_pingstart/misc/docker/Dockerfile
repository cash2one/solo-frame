FROM registry.ahaflow.com:5000/solo/runtime-base

MAINTAINER Mush Mo <mush@pandorica.io>

# update
RUN apt-get update && apt-get install -y \
    git \
    python-dev \
    vim \
    python-pip \
    libfreetype6-dev \
    libjpeg8-dev \
    && rm -rf /var/lib/apt/lists/*

ADD ./requirement.txt /home/psrun/requirement.txt

RUN pip install -r /home/psrun/requirement.txt

ADD ./code /home/runtime/new_pingstart
ADD ./entrypoint /home/runtime/new_pingstart/app/new_pingstart/entrypoint

RUN chown -R runtime:runtime /home/runtime

WORKDIR /home/runtime/new_pingstart
USER runtime

EXPOSE 20000

ENTRYPOINT ["/home/runtime/new_pingstart/app/new_pingstart/entrypoint"]

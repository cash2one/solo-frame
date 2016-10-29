FROM registry.ahaflow.com:5000/solo/runtime-base

MAINTAINER Mush Mo <mush@pandorica.io>

RUN apt-get update && apt-get install -y \
    git \
    python-dev \
    vim \
    python-pip \
    libfreetype6-dev \
    libjpeg8-dev \
    gearman-job-server \
&& rm -rf /var/lib/apt/lists/*

RUN wget https://bootstrap.pypa.io/ez_setup.py -O - | python

ADD ./requirements.txt /home/runtime/requirement.txt
RUN pip install -r /home/runtime/requirement.txt

ADD ./code /home/runtime/leadhug
ADD ./entrypoint /home/runtime/leadhug/app/leadhug/entrypoint

RUN chown -R runtime:runtime /home/runtime

WORKDIR /home/runtime/leadhug
USER runtime

EXPOSE 20000

ENTRYPOINT ["/home/runtime/leadhug/app/leadhug/entrypoint"]

FROM python:3

ADD files/foo.txt /tmp/files/
ADD files/bar.txt /tmp/files/

# Should be pillar derp
ADD pillars/funtimes.py /tmp/pillars/

ENV EMAIL user@example.com
RUN cd /tmp/files && git init && git add . && git commit -m 'initial commit' && git clone --bare . /repos/files.git && mv /repos/files.git/hooks/post-update.sample /repos/files.git/hooks/post-update
RUN cd /tmp/pillars && git init && git add . && git commit -m 'initial commit' && git clone --bare . /repos/pillars.git && mv /repos/pillars.git/hooks/post-update.sample /repos/files.git/hooks/post-update

WORKDIR /repos/files.git
RUN git --bare update-server-info
WORKDIR /repos/pillars.git
RUN git --bare update-server-info

RUN mv /tmp/files /repos && mv /tmp/pillars/ /repos/

WORKDIR /repos

EXPOSE 8000
ENTRYPOINT ["/usr/local/bin/python3", "-m", "http.server"]

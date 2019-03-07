FROM centos:latest as base

RUN yum -y update && \
    yum -y install python-ldap python-setproctitle epel-release git && \
    yum -y install https://repo.saltstack.com/yum/redhat/salt-repo-2018.3-1.el7.noarch.rpm  && \
    yum clean all

FROM base

RUN yum -y install salt-master virt-what python-pygit2 python-pip && \
    yum clean all

RUN pip install pika

ADD entrypoint.sh /entrypoint.sh
RUN chmod 755 /entrypoint.sh

ADD master.conf /etc/salt/master

RUN useradd saltapi
RUN echo "salt" | passwd --stdin saltapi

EXPOSE 4505/tcp 4506/tcp

ENTRYPOINT ["/entrypoint.sh"]

CMD ["salt-master", "-l", "info"]

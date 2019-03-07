FROM centos:latest as base

RUN yum -y update && \
    yum -y install python-ldap python-setproctitle epel-release git && \
    yum -y install https://repo.saltstack.com/yum/redhat/salt-repo-2018.3-1.el7.noarch.rpm  && \
    yum clean all

FROM base

RUN yum -y install salt-minion virt-what python-pygit2 python-pip && \
    yum clean all

RUN pip install pika

CMD ["salt-minion", "-l", "info"]

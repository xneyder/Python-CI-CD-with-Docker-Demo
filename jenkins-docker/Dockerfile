FROM jenkinsci/blueocean
USER root

WORKDIR /tmp
COPY ./conf/sasl_passwd /etc/postfix/sasl_passwd
COPY ./conf/ca-bundle.crt /etc/ssl/certs/
COPY ./conf/main.cf ./
RUN apk add py-pip
RUN apk --no-cache add ca-certificates gettext postfix rsyslog supervisor mailx
RUN pip install docker-compose


RUN cat main.cf >> /etc/postfix/main.cf
RUN postmap /etc/postfix/sasl_passwd
RUN chown root:postfix /etc/postfix/sasl_passwd
RUN chmod 640 /etc/postfix/sasl_passwd
CMD ["postfix", "-c", "/etc/postfix", "start"]



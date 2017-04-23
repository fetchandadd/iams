FROM python:3.4.6-onbuild

MAINTAINER Tim Tegler <mail@timtegeler.de>

WORKDIR /usr/src/app/src

# Activate production config
RUN mv cherrypy.production.conf cherrypy.conf

CMD [ "python", "app.py" ]


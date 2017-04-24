FROM python:3.5.3-onbuild

MAINTAINER Tim Tegler <mail@timtegeler.de>

WORKDIR /usr/src/app/src

# Activate production config
RUN mv cherrypy.production.conf cherrypy.conf

CMD [ "python", "app.py" ]


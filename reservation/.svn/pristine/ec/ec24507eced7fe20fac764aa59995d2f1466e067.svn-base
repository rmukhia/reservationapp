FROM python:2
ADD . /app
RUN apt-get update && apt-get install -y nginx  &&\
	cd /app && mkdir logs && \
	cp nginx.conf /etc/nginx/nginx.conf && \ 
	cp server/reservation/settings.production.py server/reservation/settings.py && \
	pip install -r venv_packages
WORKDIR /app/server
CMD service nginx restart && bash gunicorn_start.sh
EXPOSE 9000
	 



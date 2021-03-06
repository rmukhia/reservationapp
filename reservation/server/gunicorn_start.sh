NAME="reservation"                              #Name of the application (*)
DJANGODIR=/app/server/             		# Django project directory (*)
SOCKFILE=/app/server/unix.sockfile        	# we will communicate using this unix socket (*)
DJANGO_SETTINGS_MODULE=reservation.settings             # which settings file should Django use (*)
DJANGO_WSGI_MODULE=reservation.wsgi                     # WSGI module name (*)


export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --bind=unix:$SOCKFILE \
  --access-logfile /app/logs/gunicorn-access.log \
  --error-logfile /app/logs/gunicorn-error.log

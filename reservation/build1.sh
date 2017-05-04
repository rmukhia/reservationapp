pip install virtualenv
virtualenv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r venv_packages
python manage.py bower install
python manage.py collectstatic --no-input


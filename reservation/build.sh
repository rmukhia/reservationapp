# Requirements
# * nodejs, bower
# * python, pip
# * libmysqlclient-dev python-dev
# * internet connection

pip install virtualenv

svn update
virtualenv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r venv_packages
pushd server
python manage.py bower install
python manage.py collectstatic --no-input
popd
docker build -t reservation-app .

rm static -rf

# Requirements
# * nodejs, bower
# * python, pip
# * libmysqlclient-dev python-dev
# * internet connection
#svn update
virtualenv venv
source venv/bin/activate
pip install -r venv_packages
pushd server
python manage.py bower install
popd

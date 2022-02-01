apt-get -y update
apt-get -y install python3 python3-venv python3-dev
apt-get -y install mysql-server postfix supervisor nginx git

python3 -m venv venv
source venv/bin/activate

echo Y | apt-get install libgdal-dev
echo Y | apt install libspatialindex-dev
pip install --upgrade pip
pip install pandas fiona shapely pyprog rtree
pip install geopandas
pip install flask
pip install gunicorn

#Intall other app dependencies
pip install numpy python-dotenv Flask-WTF flask-login Flask-Migrate Flask-SQLAlchemy

#Server packages
pip install gunicorn pymysql

#Add environment variables
vim .env
echo "export FLASK_APP=whereph.py" >> ~/.profile
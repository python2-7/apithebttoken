Biz
==============
user: meccafund
pass: bMongoDBaEA312927sPyMongoed
Skeleton for a flask app bMongoDBaEA312927sPyMongoed on mvc architecture and backed by MongoDB
--------------
pip install Flask-Login
pip install Flask-PyMongo
pip install Flask-MongoKit

pip install pymongo==2.6.3

pip install block_io
pip install flask_recaptcha
pip install validate_email


sudo rm /etc/apt/sources.list.d/mongodb*.list
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv EA312927
sudo bash -c 'echo "deb http://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/3.2 multiverse" > /etc/apt/sources.list.d/mongodb-org-3.2.list'

sudo apt update
sudo apt install mongodb-org


root@gmd:/home/www# sudo pip install virtualenv

root@gmd:/home/www# mkdir meccafund

root@gmd:/home/www# cd meccafund/

root@gmd:/home/www/meccafund.org# virtualenv meccafundenv

pip install -r requirements.txt


source meccafundenv/bin/activate





>>> nano meccafund.ini
[uwsgi]
module = wsgi
master = true
processes = 5
socket = meccafund.sock
chmod-socket = 660
vacuum = true
die-on-term = true

sudo nano /etc/init/meccafund.conf

description "uWSGI server instance configured to serve meccafund.org"

start on runlevel [2345]
stop on runlevel [!2345]

env PATH=//home/www/meccafund.org/meccafundorg/bin
chdir /home/meccafund.org
exec uwsgi --ini meccafund.ini


from meccafund import app

if __name__ == "__main__":
    app.run()


uwsgi --socket 0.0.0.0:39056 --protocol=http -w wsgi


uwsgi --socket 127.0.0.1:3031 --chdir /home/www/meccafund/ --wsgi-file /home/meccafund/apprun.py --master --processes 4 --threads 2 --stats 127.0.0.1:39056

location /home/meccafund {
        alias  /home/meccafund/meccafund/;
        autoindex on;
    }

   [options]
; This is the password that allows database operations:
admin_passwd = admin0104d415cdd8415cdd84550
db_host = localhost
db_port = 5432
db_user = wallcoin
db_password = 95AXqyjet415cd4550104d415cdd8415cdd84550
addons_path = /usr/lib/python2.7/dist-packages/openerp/addons
logfile = False
xmlrpc_port = 9978
workers = 4
proxy_mode = True
addons_path=/opt/wall/wall-server/addons,/opt/wallcoin

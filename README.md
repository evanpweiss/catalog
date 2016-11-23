# Linux Server Configuration:  Hosting Item Catalog

The goal of the Linux Server Configuration project is to configure an Amazon EC2 server to host a database-backed web application.  The requirements for this project are described [here] (https://review.udacity.com/#!/rubrics/7/view).  The hosted application is built using Flask backed by a PostgreSQL database.  It makes extensive use of the sqlalchemy ORM to query the database.

Linux Server Configuration is the final project of the Udacity Configuring Linux Web Servers course.


## EC2 Instance Information

Server IP: 35.160.225.46
Application web address: http://ec2-35-160-225-46.us-west-2.compute.amazonaws.com/
SSH Port: 2200

## Quickstart

To view the working catalog application, simply navigate to http://ec2-35-160-225-46.us-west-2.compute.amazonaws.com/.  You can view all items without logging in, but much authenticate with a valid Google account in order to create new items.

### Software Installed
* Updated all package lists
* Upgraded all installed packages
* apt-get install apache2
* apt-get install libapache2-mod-wsgi
* apt-get install python-pip
* apt-get install postgresql
* apt-get install git
* apt-get install python-psycopg2
* pip install flask
* pip install sqlalchemy
* pip install google-api-python-client (for oauth2client module)
* pip install bleach

### Summary of Configurations Made
* Set root password
* Created grader user, set password, and added sudoers.d config
* Installed public key for grader
* Changed SSH port to 2200 and changed PermitRootLogin to no
* Configured UFW to default disable incoming, default allow outgoing, and enable incoming traffic on ports 2200, 80 and 123
* Cloned git repository to /var/www/catalog
* Launched psql management interface and ran \i  /var/www/catalog/catalog.sql to create tables and pre-populate categories
* Created catalog_user psql user as a member of catalog group and set a password
* GRANT SELECT ON categories TO catalog;
* GRANT SELECT, INSERT, UPDATE, DELETE ON item_table TO catalog;
* GRANT SELECT, INSERT, UPDATE ON users TO catalog;
* GRANT USAGE, SELECT ON SEQUENCE users_id_seq to catalog;
* GRANT USAGE, SELECT ON SEQUENCE item_table_id_seq to catalog;
* Configured apache2 virtual host and pointed it to use wsgi script alias /var/www/catalog/catalog.wsgi (cloned from github repo)
* Created client_secrets.json file in /var/www/catalog/ and populated with information from Google cloud console
* Restarted apache2 service and tested application

### Third-party Resources Used
* http://www.ducea.com/2006/06/18/linux-tips-password-usage-in-sudo-passwd-nopasswd/ - referenced to figure out the correct pattern for sudoers.d file to force sudo password prompt (i.e. PASSWD:ALL vs NOPASSWD:ALL)
* http://www.saltycrane.com/blog/2010/02/how-install-pip-ubuntu/ - reference to figure out the correct package name for for python-pip
* https://www.postgresql.org/docs/ - referenced for commands to create users and groups, set passwords, and grant permissions on tables
* http://stackoverflow.com/questions/9325017/error-permission-denied-for-sequence-cities-id-seq-using-postgres - referenced for how to grant permissions to postgres sequences.
* https://discussions.udacity.com/t/no-wsgi-daemon-process/30798/7 - referenced for information on how to configure catalog.wsgi and virtualhosts
* http://docs.sqlalchemy.org/en/latest/orm/extensions/automap.html - referenced for information how to make sqlalchemy work with Postgres, especially useful was information on how to auto-map classes.

## Versioning

This is version 1.0 of my Linux Server Configuration project.

## Credits

Credit for this Readme format goes to Bootstrap's excellent [README.md] (https://github.com/twbs/bootstrap/blob/master/README.md)

## Creators

**Evan Weiss**

* <https://www.linkedin.com/in/evanpweiss>

## Copyright and license

Code released under [the MIT license](https://opensource.org/licenses/MIT):
Copyright (c) 2016, Evan Weiss

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
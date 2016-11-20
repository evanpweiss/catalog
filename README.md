# Item Catalog

The goal of the Item Catalog project is to create a web application which supports creation, reading, updating and deleting a catalog of items.  The requirements for this project are described [here] (https://review.udacity.com/#!/rubrics/5/view).  This application is built using Flask backed by a sqlite database.  It makes extensive use of the sqlalchemy ORM to query the sqlite database.

Item Catalog is the final project of the Udacity Full Stack Foundations course.


## Quick start

In order to use the included files, you will need to install sqlite3 and sqlalchemy.  I recommend using the Vagrant virtual machine provided by Udacity as described [here] (https://www.udacity.com/wiki/ud197/install-vagrant).  Once you have installed Vagrant:
1. Unzip the files in the attached archive into a folder on the virtual machine
2. Launch the virtual machine using the command `vagrant up`
3. Log in to the virutal machine using the command `vagrant ssh`
4. Run database_setup.py using the command `python database_setup.py`.  This will create a sqlite database named "new_catalog.db"
5. Run populate_categories.py using the command `python populate_categories.py`.  This will pre-populate the application with 10 default categories.  You can provide your own categories by modifying the array of category names on lines 13 - 22.
6. Run project.py using the command `python project.py`.  This will server the catalog app locally on port 5000.
7. To access the application in your browser, simply navigate to http://localhost:5000.

You can now create, view, edit, and delete items.  Note that you must log in with a Google ID in order to create, edit and delete items.  You may retrieve the entire catalog (all categories and items) programmatically via the /catalog/catalog.json endpoint.  If you know an item's ID, you may retrieve details about the item programmatically via the /catalog/items/ITEM_ID.json endpoint.


### What's included

Within this archive, you'll find the following files:

* database_setup.py (creates a sqlite database with User, Category and Item tables)
* populate_categories.py (populates the Category table with 10 pre-defined categories)
* project.py (contains all logic to present the Item Catalog web application, including user authentication and authorization)
* client_secrets.json (contains secret keys necessary for the application to authenticate users via Googl oAuth.  The contents of this file should never be made public for production applications, but it is included here for the assignment)
* /static (this folder contains a CSS file to style the application)
* /templates (this folder contains all HTML templates used in the application.  Templates use Jinja2 syntax.)
* README.md (this readme file!)


## Versioning

This is version 1.0 of my Tournament Results project.

## Credits

I leveraged the templates and example code provided as part of the Full Stack Foundations course extensively (in-particular the oAuth methods and templates).  Massive thanks goes to Lorenzo and the rest of the awesome crew at Udacity!  Original source can be found [here] (https://github.com/udacity/ud330)

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
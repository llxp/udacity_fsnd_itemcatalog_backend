# Item Catalog Project

## SETUP ##

Simply run:
```sh
pip3 install -r requirements.txt
```
or:
```sh
python3 -m "pip" install -r requirements.txt
```

instead of ```python3``` command:
```py``` or ```python``` can also be run (if python 3 is installed)

## Running the App ##

To start the app execute the following command:
On Windows:
```sh
py .\app.py
```

Everywhere else:
```sh
python3 .\app.py
```

if nothing is changed, this app will be reachable on the url:
http://localhost:5000

## LICENSE ##
This project is licensed under the MIT License - see the LICENSE.md file for details

### Files: ###

#### This project consists of 7 python files: ####

app.py --> main file to start the project
authentication.py --> code for handling everything related to restapi authentication
login_session.py --> Classes for the login_session object inside of authentication.py
app_init.py --> global initialization objects which are shared between some of the parts of this project
Models.py --> the database models
item_catalog_api.py --> rest endpoint for managing the page using rest calls
item_catalog_frontend.py --> the flask/jinja frontend

#### This project consists of 3 html files: ####

base.html  --> master template which is extended using index.html and login.html
index.html --> template for the start page
login.html --> template for the login page

#### THis project consists of 9 javascript files:

common.js --> code which is shared across the project
search.js --> code for handling the search in the top middle of the page
login.js --> code for handling the login process
add_category.js --> code for adding a new category to the catalog
edit_category.js --> code for editing a selected category
delete_category.js --> code for deleting a selected and edited category
add_item.js --> code for adding a new item to the catalog
edit_item.js --> code for editing a selected item
delete_item.js --> code for deleting a selected and edited item
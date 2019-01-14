# Item Catalog Project

## SETUP ##
#### To use this project you need python 3 installed ####
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

app.py --> main file to start the project</br>
authentication.py --> code for handling everything related to restapi authentication</br>
login_session.py --> Classes for the login_session object inside of authentication.py</br>
app_init.py --> global initialization objects which are shared between some of the parts of this project</br>
Models.py --> the database models</br>
item_catalog_api.py --> rest endpoint for managing the page using rest calls</br>
item_catalog_frontend.py --> the flask/jinja frontend</br>

#### This project consists of 3 html files: ####

base.html  --> master template which is extended using index.html and login.html</br>
index.html --> template for the start page</br>
login.html --> template for the login page</br>

#### This project consists of 9 javascript files:

common.js --> code which is shared across the project</br>
search.js --> code for handling the search in the top middle of the page</br>
login.js --> code for handling the login process</br>
add_category.js --> code for adding a new category to the catalog</br>
edit_category.js --> code for editing a selected category</br>
delete_category.js --> code for deleting a selected and edited category</br>
add_item.js --> code for adding a new item to the catalog</br>
edit_item.js --> code for editing a selected item</br>
delete_item.js --> code for deleting a selected and edited item</br>
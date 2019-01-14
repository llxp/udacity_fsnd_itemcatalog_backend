# Item Catalog Project

## SETUP ##
#### To use this project you need to have python 3 installed ####
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

### Setup of the authentication/authorization process ####
1. please go to the google API console under https://console.developers.google.com
2. There go to Credentials (On the left side menu)
3. If you have already created an app there, you can reuse this app and skip to step 9.
4. If you haven't created an app already or don't want to reuse the existing app:
5. Click on the button "Create credentials":
6. Then click on "OAuth client ID"
7. As the "Application type" select "Web application"
8. Enter a name for this app which you haven't used yet
9. Under "Authorized JavaScript origins" add the host of the flask web app:
10. If nothing was changed yet the default host will be:
> ```http://localhost:5000```
11. If you also want to use some rest client like angularJS, you have to add the host of this app aswell:
> Angular (7/CLI) uses per default ```http://localhost:4200```
12. Under "Authorized redirect URIs" add the redirect uri of the flask application:
13. If nothing was changed yet the default redirect uri will be:
> ```http://localhost:5000/user/gconnect```
14. If you want to use some rest client like anguluarJS, you have to add the redirect uri aswell:
> e.g. ```http://localhost:4200/user/gconnect```
15. Please copy your own copy of the client_secrets.json to the root directory of this project:
    > for this to do you have to press on the button "Download JSON" On the top and name the file "client_secrets.json".
16. Do not forget to press on "Save" when finished editing the app in the google API console

#### Setup of a rest client like AngularJS ####
If you want to use an rest client like AngularJS here are some steps how to do this (coveres only the authenticataion process):
1. Do the steps mentioned above specific for the angular app to add the host and redirect URIs
2. Create a new route in the routeConfig.ts (this example is only working if you are using Routing in your app)
3. set as the path the same you entered for the redirect URI e.g. ```http://localhost:4200/user/gconnect```
4. set as the "component" parameter the component you are using to show the login page and to react to the parameters added by the google authorization process (get parameter 'code', etc...)
5. An example of such a component is given [here](https://gist.github.com/llxp/533e821fe903fb2953cdfe17ed20ddd9).
6. Create a new service e.g. 'login.service.ts' using the cli: ```ng g service login```
7. If you want to get an example how to implement this service hava a look at this [example](https://gist.github.com/llxp/b55f712b997460fa645733c4050edcb6).
8. At the very least if you have changed the redirect uri from step 2/3 change line 125 in the ["authentication.py"](https://github.com/llxp/udacity_fsnd_itemcatalog_backend/blob/master/authentication.py) file

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

## USAGE ##

if nothing is changed, this app will be reachable on the url:
http://localhost:5000

The following actions can only be made, when logged in:<br/>
1. A category can be added by pressing the plus button under the categories
2. A category can be edited by pressing on the edit button under the items, when a category is selected
3. A category can be deleted by going into the category edit mode and then pressing the trash button
4. An new item can be added to the catalog by selecting a category and pressing the plus button under the items list
5. An item can be edited by selecting an item and pressing the edit button under the description of the item
6. An item can be deleted by going into the item edit mode and then pressing the trash button

## LICENSE ##
This project is licensed under the MIT License - see the [LICENSE](https://github.com/llxp/udacity_fsnd_itemcatalog_backend/blob/master/LICENSE) file for details

### Files: ###

#### This project consists of 7 python files (in / directory of the project): ####

[app.py](https://github.com/llxp/udacity_fsnd_itemcatalog_backend/blob/master/app.py) --> main file to start the project<br/>
[authentication.py](https://github.com/llxp/udacity_fsnd_itemcatalog_backend/blob/master/authentication.py) --> code for handling everything related to restapi authentication<br/>
[login_session.py](https://github.com/llxp/udacity_fsnd_itemcatalog_backend/blob/master/login_session.py) --> Classes for the login_session object inside of authentication.py<br/>
[app_init.py](https://github.com/llxp/udacity_fsnd_itemcatalog_backend/blob/master/app_init.py) --> global initialization objects which are shared between some of the parts of this project<br/>
[Models.py](https://github.com/llxp/udacity_fsnd_itemcatalog_backend/blob/master/Models.py) --> the database models<br/>
[item_catalog_api.py](https://github.com/llxp/udacity_fsnd_itemcatalog_backend/blob/master/item_catalog_api.py) --> rest endpoint for managing the page using rest calls<br/>
[item_catalog_frontend.py](https://github.com/llxp/udacity_fsnd_itemcatalog_backend/blob/master/item_catalog_frontend.py) --> the flask/jinja frontend<br/>

#### This project consists of 3 html files (in /templates directory of the project): ####

[base.html](https://github.com/llxp/udacity_fsnd_itemcatalog_backend/blob/master/templates/base.html)  --> master template which is extended using index.html and login.html<br/>
[index.html](https://github.com/llxp/udacity_fsnd_itemcatalog_backend/blob/master/templates/index.html) --> template for the start page<br/>
[login.html](https://github.com/llxp/udacity_fsnd_itemcatalog_backend/blob/master/templates/login.html) --> template for the login page<br/>

#### This project consists of 9 javascript files (in /static directory of the project): ####

[common.js](https://github.com/llxp/udacity_fsnd_itemcatalog_backend/blob/master/static/common.js) --> code which is shared across the project<br/>
[search.js](https://github.com/llxp/udacity_fsnd_itemcatalog_backend/blob/master/static/search.js) --> code for handling the search in the top middle of the page<br/>
[login.js](https://github.com/llxp/udacity_fsnd_itemcatalog_backend/blob/master/static/login.js) --> code for handling the login process<br/>
[add_category.js](https://github.com/llxp/udacity_fsnd_itemcatalog_backend/blob/master/static/add_category.js) --> code for adding a new category to the catalog<br/>
[edit_category.js](https://github.com/llxp/udacity_fsnd_itemcatalog_backend/blob/master/static/edit_category.js) --> code for editing a selected category<br/>
[delete_category.js](https://github.com/llxp/udacity_fsnd_itemcatalog_backend/blob/master/static/delete_category.js) --> code for deleting a selected and edited category<br/>
[add_item.js](https://github.com/llxp/udacity_fsnd_itemcatalog_backend/blob/master/static/add_item.js) --> code for adding a new item to the catalog<br/>
[edit_item.js](https://github.com/llxp/udacity_fsnd_itemcatalog_backend/blob/master/static/edit_item.js) --> code for editing a selected item<br/>
[delete_item.js](https://github.com/llxp/udacity_fsnd_itemcatalog_backend/blob/master/static/delete_item.js) --> code for deleting a selected and edited item<br/>

#### This project consts of 3 css files (in /static directory of the project) ####
[style.css](https://github.com/llxp/udacity_fsnd_itemcatalog_backend/blob/master/static/style.css) --> custom style for the index.html and login.html templates
[boostrap.css](https://github.com/llxp/udacity_fsnd_itemcatalog_backend/blob/master/static/boostrap.css) --> own copy of the bootstrap.css file because the default flask-bootstrap css file has some errors or is outdated
[font-awesome.css](https://github.com/llxp/udacity_fsnd_itemcatalog_backend/blob/master/static/font-awesome.css) --> own copy of font-awesome
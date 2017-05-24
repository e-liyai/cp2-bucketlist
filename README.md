[![Build Status](https://travis-ci.org/Andela-eugene/cp2-bucketlist.svg?branch=master)](https://travis-ci.org/Andela-eugene/cp2-bucketlist) [![Coverage Status](https://coveralls.io/repos/github/Andela-eugene/cp2-bucketlist/badge.svg?branch=ft-bucketlist-items)](https://coveralls.io/github/Andela-eugene/cp2-bucketlist?branch=ft-bucketlist-items) [![Code Health](https://landscape.io/github/Andela-eugene/cp2-bucketlist/master/landscape.svg?style=plastic)](https://landscape.io/github/Andela-eugene/cp2-bucketlist/master) [![license](https://img.shields.io/github/license/mashape/apistatus.svg)](https://github.com/Andela-eugene/cp2-bucketlist/blob/master/LICENSE.txt) [![PyPI](https://img.shields.io/pypi/pyversions/Django.svg?style=plastic)]() [![Codacy Badge](https://api.codacy.com/project/badge/Grade/7a238c181fd54ce5b2d8d68f283b1024)](https://www.codacy.com/app/Andela-eugene/cp2-bucketlist?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Andela-eugene/cp2-bucketlist&amp;utm_campaign=Badge_Grade)
# Bucketlist

Bucketlist is a Flask API application that helps individuals keep track of that elusive white whale.
The application allows users to list activities they'd like to do before they die. 
This API provides endpoints facilitating registration, login, create and manage bucket lists and their items.

## Installation

Clone this repo: 

```
$ git clone https://github.com/https://github.com/Andela-eugene/cp2-bucketlist.git
```

Change into the bucketlist directory:

```
$ cd bucketlist
```

Create the bucketlist vitual environment:

> Click on [this guide](http://docs.python-guide.org/en/latest/dev/virtualenvs/). 
The link will guide you create and activate the virtual environment

Install the required packages:
```
$ pip install -r requirements.txt
```

Set the required environment keys
```
$ export BUCKETLIST_SECRET_KEY="any_random_string"
$ export BUCKETLIST_SQLALCHEMY_DATABASE_URI='url_of_the_main_bucketlist_database'
$ export TEST_BUCKETLIST_SQLALCHEMY_DATABASE_URI='url_of_the_test_bucketlist_database'
```

## Application Configuration
The run environment associated with the application can either be `development`, `testing` or `production`.
The environment dictate how the application will run. This environments are setup in the `config.py` file.

## Usage

Run ```python manage.py runserver```.

### Test API
Use an API Client such as [Postman](https://chrome.google.com/webstore/detail/postman/fhbjgbiflinjbdggehcddcbncdddomop?hl=en)
 or [Insomnia](https://insomnia.rest) to test the endpoints.
 
### API Endpoints 


| Actions        | Description           | Requires Authentication |
| ------------- |:-------------:| -------------:|
| POST auth/login    | Log a user in | False |
| POST auth/register     | Register a new user | False |
| POST api/v1/bucketlists/ | Create a new bucketlist   | True |
| GET api/v1/bucketlists/      | List all created bucketlists | True |
| GET api/v1/bucketlists/`<string:bucket_id>`     | get single bucketlist | True |
| PUT api/v1/bucketlists/`<string:bucket_id>` | update single bucketlist | True |
| DELETE api/v1/bucketlists/`<string:bucket_id>`      | Delete a single bucketlist | True |
| POST api/v1/bucketlists/`<string:bucket_id>`/items      | Create a new item in a bucketlist | True |
| PUT api/v1/bucketlists/update-item/`<string:item_id>` | Update an item in a bucketlist | True |
| DELETE api/v1/bucketlists/items/`<string:item_id>`     | Delete an item in a bucketlist | True |
| GET /api/v1/bucketlists/items/`<string:bucket_id>`    |   Get items in a bucketlist       | True |
| GET api/v1/users/     |   Get all users       | True |
| GET api/v1/user/`<string:user_id>`   |   Get a single user   | True |
| PUT api/v1/user/`<string:user_id>`   |   Update a user       | True |
| DELETE api/v1/delete_user/`<string:user_id>`    | Delete a user | True |

## Built With...
* [Flask](http://flask.pocoo.org/)
* [Flask-SQLAlchemy](http://flask-sqlalchemy.pocoo.org/2.1/)

## License

### The MIT License (MIT)

Copyright (c) 2017 [Eugene Liyai](https://github.com/Andela-eugene).

> Permission is hereby granted, free of charge, to any person obtaining a copy
> of this software and associated documentation files (the "Software"), to deal
> in the Software without restriction, including without limitation the rights
> to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
> copies of the Software, and to permit persons to whom the Software is
> furnished to do so, subject to the following conditions:
>
> The above copyright notice and this permission notice shall be included in
> all copies or substantial portions of the Software.
>
> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
> IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
> FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
> AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
> LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
> OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
> THE SOFTWARE.

# Casting Agency web service

## Introduction

This is a basic crud app that allows a media company to manage ```actors``` and ```movies``` resources. This app uses:
- flask for backend service
- auth0 for third party authentication
- postgresql for database

## Running project locally

1. Create a database for local unitesting
   
   Login to the psql console and create a database
   ```bash
   psql -U postgres
   psql> CREATE DATABASE capstone_test;
   ```

2. Create a setup.sh file it should have the following contents:

```bash
#!/bin/sh
# Setup data base path
export DATABASE_URL="postgresql://{user}:{pw}@localhost:5432/{database_name}"
# Setup Auth0 credentials
export AUTH0_DOMAIN="gunnvantcoffee.us.auth0.com"
export API_AUDIENCE="casting"
export ALGORITHMS="RS256"
```


3. Now install all the dependencies in a virtual environment using ```pip intsall -r requirements.txt```
4. Now run ```python test.py``` to run all the unitests
5. In order to run the app first run the migrations
   
   ```bash
    python manage.py db init
    python manage.py db migrate
   ```
6. Then run the app:

```bash
export FLASK_APP=run_local
export FLASK_ENV=development
export DEBUG=1
flask run
```
## Users and permissions
There are three users who have been mapped to three roles:
- User1
     -   Username: castingudacity@gmail.com
     -   Password: casting@1234
     -   Permissions: get:actors, get:movies
     -   Role: Casting Assistant
 - User2
     - Username: directorudacity@gmail.com
     - Password: director@123
     - Permissions: get:actors, get:movies, post:actors, patch:actors, delete:actors,  patch:movies
     - Role: Casting Director
 - User3
   - Username: producer@gmail.com
   - Password: producer@123
   - Permissions: get:movies, get:actors, delete:movies, delete:actors, post:movies, post:actors, patch: movies, patch:actors
   - Role: Executive Producer
## Hosting instructions

The app is hosted on heroku at {url}--> todo
This app can also be hosted on any linux box. Make sure a postgres server is running and a database for the use by this app is available.

Follow steps 1 to 5 given in **Running Locally** section. To run the actual server use gunicorn

```bash
gunicorn --bind 0.0.0.0:5000 server:app

```

## Project Structure
```
📦casting
 ┣ 📂app
 ┃ ┣ 📂auth
 ┃ ┃ ┣ 📜auth.py ## Provides requires_auth decorator
 ┃ ┃ ┗ 📜__init__.py
 ┃ ┣ 📂models
 ┃ ┃ ┣ 📜models.py ## Manages tables and db utils
 ┃ ┃ ┗ 📜__init__.py
 ┃ ┣ 📂routes
 ┃ ┃ ┣ 📜routes.py ## Logic for endpoints
 ┃ ┃ ┗ 📜__init__.py
 ┃ ┗ 📜__init__.py
 ┣ 📜manage.py ## Manages migrations
 ┣ 📜README.md
 ┣ 📜requirements.txt
 ┣ 📜run_local.py ## Runs local development server
 ┣ 📜setup.sh ## Environment Variables
 ┗ 📜tests.py ## Unittests
```

## API Endpoints and RBAC controls

**GET/auth**

Login to the app, this takes you to the login page, using user credentials for User1 or User2 or User3 given above one can obtain tokens

**GET/status**

Health check for app returns the following json

```json
{
    "healthy":true
}

```

**GET/actors**

This returns a json object with id,age,gender,count and a Boolean on the success of the call. A sample json is given below:

```json

{
    "count":2
    "success":true
    "actors":
        [
            {
                "id":1,
                "name":"bob",
                "age":32,
                "gender":"Male"
            },
            {
                "id":2
                "name":"mary",
                "age":23,
                "gender":"Female"
            }   
        ]
}    

```

**GET /movies**

This will return the id, title and release date. See example below

```json
{
    "count":2,
    "success":true,
    "movies":
            [
                {
                    "id":1,
                    "title":"movie1",
                    "release_date":"26/11/2021"
                },
                {
                    "id":3,
                    "title":"movie3",
                    "release_date":"26/11/2021"
                }        
            ]
}
```
**DELETE /actors/id**

Deletes an actor from the database based his/her id

The end point can be reached as

```bash
 curl -H "Authorization: Bearer mytoken123" -X DELETE http://{{domian}}/api/actors/1 
```
If the actor with actor id exists the following response will be shown

```json
{
    "success":true
    "deleted":1
}
```
If the actor doesn't exist a 404 response will be sent back

**DELETE /movies/id**

This will delete the movie given the id. This endpoint can be reached as:

```bash
curl -H "Authorization: Bearer mytoken123" -X DELETE http://{{domian}}/api/movies/1
```
If the movie with given id exists, then the following response will be sent back:

```json
{
    "success":true,
    "deleted":1
}

``` 

If the movie id doesn't exist a 404 will be sent

**POST /actors**

This will create a new actor resource. The body will be json with fields such as name,age and gender. The field gender can only take values *male* or *female* and can't be empty.

The end point can be reached as follows:

```bash
curl -H "Content-Type: application/json" -H "Authorization: Bearer mytoken123" \
  --request POST \
  --data '{"name":"xyz","age":30,"gender":"male"}' \
  http://{{domain}}/api/actors
```
If the actor resource is successfully created following json response will be sent:

```json
{
    "success":true,
    "created":3
}
```
In case the resource can't be created a 422 error code will be raised

**POST /movies**

This will create a new movie resource. The body will be json with fields such as title and release_date (dd/mm/yyyy). 

The end point can be reached as follows:

```bash
curl -H "Content-Type: application/json" -H "Authorization: Bearer mytoken123"
  --request POST \
  --data '{"title":"xyz","release_date":"20/11/2020"}' \
  http://{{domain}}/api/movies
```
If the movie resource is successfully created following json response will be sent:

```json
{
    "success":true,
    "created":3
}
```

In case the the resource can't be created a 422 will be raised 

**PATCH /actors/id**

This will update an actor resource. The body will be json with fields such as name or age or gender . The field gender can only take values *male* or *female* and can't be empty.


```bash
curl -H "Content-Type: application/json" -H "Authorization: Bearer mytoken123"
  --request PATCH \
  --data '{"name":"xyz","age":30}' \
  http://{{domain}}/api/actors
```
If the actor resource is successfully created following json response will be sent:

```json
{
    "success":true,
    "updated":3
}
```

In case the update fails a 422 will be raised

**PATCH /movies/id**

This will update a movie resource. The body will be json with fields such as title and release date


```bash
curl -H "Content-Type: application/json" -H "Authorization: Bearer mytoken123"
  --request PATCH \
  --data '{"title":"xyz","release_date":"20/11/2020"}' \
  http://{{domain}}/api/movies
```
If the movie resource is successfully created following json response will be sent:

```json
{
    "success":true,
    "updated":3
}
``` 
In case the movie resource can't be updated a 422 will be raised.
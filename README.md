# Capstone
-----------------

## Introduction

Capstone is a Casting Agency  that is responsible for creating movies and managing and assigning actors to the movies. This agency lets you list new actors, movies, and list movies with the release dates.


## Overview

This app is fully functional and is capable of doing the following, using a PostgreSQL database:

* creating new movies and actors.
* Delete new movies and actors.
* Update actors and movies information.

## Tech Stack (Dependencies)

### 1. Backend Dependencies
Tech stack will include the following:
 * **virtualenv** as a tool to create isolated Python environments
 * **SQLAlchemy ORM** to be our ORM library of choice
 * **PostgreSQL** as our database of choice
 * **Python3** and **Flask** as our server language and server framework
 * **Flask-Migrate** for creating and running schema migrations
You can download and install the dependencies mentioned above using `pip` as:
```
pip install virtualenv
pip install SQLAlchemy
pip install postgres
pip install Flask
pip install Flask-Migrate
pip install Flask-Script
pip install psycopg2-binary
```
#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/src` directory and running:
# You should have requirements.txt  available
```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.


##### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. Since we want you to focus on auth, we handle the heavy lift for you in `./src/database/models.py`. We recommend skimming this code first so you know how to interface with the Drink model.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

### Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server in development

From within the `./src` directory first ensure you are working using your created virtual environment.

Each time you open a new terminal session, run:

```bash
export FLASK_APP=api.py;
```

All the Environment variables are mentioned in the file setup.sh to run locally.
execute
# You should have setup.sh  available
chmod +x setup.sh
source setup.sh

To run the server, execute:
```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.
### Setup Auth0
Capstone operates using three roles 
1.**CastingAgency**
  able to retrieve information about movies and actors
   - `get:movies`
   - `get:actors`

2.**Casting Director**
able to retrieve ,add and modify movies and actors.Permitted to delete and actor.
   - `get:actors`
   - `get:movies`
   - `post:actors`
   - `post:movies`
   - `patch:actors`
   - `patch:movies`
   - `delete:actors`

3.**Casting Producer**
able to retrieve ,add and modify movies and actors.Permitted to delete actors and movies.
   - `get:actors`
   - `get:movies`
   - `post:actors`
   - `post:movies`
   - `patch:actors`
   - `patch:movies`
   - `delete:actors`
   - `delete:movies`

### Deployment configuration
Application is hosted on Heroku platform.
Heroku platfrom enables to configure Environment variables in GUI 
 Heroku dashboard >> Particular App >> Settings >> Reveal Config Vars


### Endpoints Description
1.*GET '/actors'*
  - This endpoint retrieves and provides the list of entire actors and their informaiton about age,gender and name.

2.*GET '/movies'*
  - This endpoint retrieves and provides the list of entire movies and informaiton of the releasedates.
 
3.*POST 'actors'*
  - This endpoint allows to insert new actor into the database and returns new list.
 
4.*POST 'movies'*
  -  This endpoint allows to insert new movie into the database and returns new list.

5.*PATCH 'actors'*
  - This endpoint allows to update existing actor into the database and returns updated actor.

6.*PATCH 'movies'*
  - This endpoint allows to update existing movie into the database and returns updated movie.
  
7.*DELETE 'actors'*
  -  This endpoint allows to delete existing actor in the database.
 
8.*DELETE 'movies'*
  -  This endpoint allows to delete existing movie in the database.

### Testing the Application
Application is hosted on Heroku platform.It is live and running at
http://mycapstoneproject2022.herokuapp.com

To run the application run
`heroku run python manage.py db upgrade --app mycapstoneproject2022`

  

from operator import itemgetter
import os,json
from unicodedata import name
from wsgiref.util import application_uri
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import true
from models import setup_db, Movies, Actors
from auth.auth import AuthError, requires_auth, get_token_auth_header


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    cors = CORS(app, resources={r"*": {"origins": "*"}})

#CORS HEaders
    @app.after_request
    def after_request(response):
        response.headers.add(
        "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
        "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,PATCH,OPTIONS"
        )
        return response

    @app.route('/')
    def get_greeting():
        excited = os.environ['EXCITED']
        greeting = "Hello" 
        if excited == 'true': 
            greeting = greeting + "!!!!! Welcome to the Capstone Project"
        return greeting

    @app.route("/movies",methods=['GET'])
    @requires_auth('get:movies')
    def retrieve_movies(payload):
        try:
            movies_collection = Movies.query.order_by(Movies.id).all()
            if len(movies_collection) == 0:
                abort(404)
            
            movie_list = [movie.format() for movie in movies_collection]
            return jsonify({'success': True, 
                    'movies': movie_list},
                    200)
        except Exception:
            abort(422)

    @app.route("/actors",methods=['GET'])
    @requires_auth('get:actors')
    def retrieve_actors(payload):
        try:
            actors_collection = Actors.query.order_by(Actors.id).all()
           
            if len(actors_collection) == 0:
                abort(404)
            
            actors_list = [actor.format() for actor in actors_collection]
            return jsonify({'success': True, 
                    'actors': actors_list},
                    200)
        except Exception:
            abort(422)
  
    @app.route("/movies", methods=['POST'])
    @requires_auth('post:movies')       
    def create_movie(payload):
        # Get the request json
        req = dict(request.json)
        try:
            newmovie = Movies(title=req.get('title'),releasedate=req.get('releasedate'))
            newmovie.insert()
            all_movies = Movies.query.all()
            new_movie_list = [movie.format() for movie in all_movies]
        except Exception:
            newmovie.rollback()
            abort(422)
        newmovie.update()
        return jsonify({'success': True, 
                    'movies': new_movie_list},
                    200)

    @app.route("/actors", methods=['POST'])
    @requires_auth('post:actors')
    def create_actor(payload):
        # Get the request json
        req = dict(request.json)
        try:
            newactor = Actors(name=req.get('name'),age=req.get('age'),gender=req.get('gender'))
            newactor.insert()
            all_actors = Actors.query.all()
            new_actors_list = [actor.format() for actor in all_actors]
        except Exception:
            newactor.rollback()
            abort(422)
        newactor.update()
        return jsonify({'success': True, 
                    'actors': new_actors_list},
                    200)

    @app.route('/actors/<int:id>', methods = ['PATCH'])
    @requires_auth('patch:actors')
    def update_actor(payload,id):
       # get the body
        req = request.get_json()

        # get the drink with requested Id
        actor = Actors.query.filter(Actors.id == id).one_or_none()

        if not actor:
            abort(404)

        try:
            req_name = req.get('name')
            req_age = req.get('age')
            req_gender = req.get('gender')

            # If name has to be updated
            if req_name:
                actor.name = req_name
            if req_age:
             actor.age = req_age
            if req_gender:
                actor.gender = req_gender

            # update the drink
            actor.update()

        except Exception:
         abort(422)
    
        return jsonify({'success': True, 'actors': [actor.format()]},200)

    @app.route('/movies/<int:id>', methods = ['PATCH'])
    @requires_auth('patch:movies')
    def update_movie(payload,id):
        # get the body
        req = request.get_json()

        # get the movie with requested Id
        movie = Movies.query.filter(Movies.id == id).one_or_none()

        if not movie:
            abort(404)

        try:
            req_title = req.get('title')
            req_releasedate = req.get('releasedate')
        
        # If name has to be updated
            if req_title:
                movie.title = req_title
            if req_releasedate:
                movie.releasedate = req_releasedate
        
            # update the movie
            movie.update()

        except Exception:
            abort(422)
    
        return jsonify({'success': True, 'movies': [movie.format()]},200)

    @app.route('/actors/<int:id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(payload,id):
        # Fetch the body
        req = request.get_json()

        # get the actor for requested Id
        actor = Actors.query.filter(Actors.id == id).one_or_none()

        if not actor:
            abort(404)

        try:
            # delete the drink
            actor.delete()
        except Exception:
            abort(422)

        return jsonify({'success': True, 'delete': id}, 200)

    @app.route('/movies/<int:id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(payload,id):
        # Fetch the body
        req = request.get_json()

        # get the movie for requested Id
        movie = Movies.query.filter(Movies.id == id).one_or_none()

        if not movie:
            abort(404)

        try:
            # delete the drink
            movie.delete()   
           
        except Exception:
            abort(422)

        return jsonify({'success': True, 'delete': id }, 200)


    # Error Handling
    '''
    Example error handling for unprocessable entity
    '''
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
        }), 422

    @app.errorhandler(404)
    def resource_not_found(error):
        return jsonify({
        "success": False,
        "error": 404,
        "message": "unprocessable"
    }), 404

    @app.errorhandler(AuthError)
    def auth_error(error):
        print(error)
        return jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.error['description']
        }), error.status_code

    @app.errorhandler(401)
    def unauthorized(error):
        print(error)
        return jsonify({
        "success": False,
        "error": 401,
        "message": 'Unathorized'
    }), 401

    @app.errorhandler(500)
    def internal_server_error(error):
        print(error)
        return jsonify({
        "success": False,
        "error": 500,
        "message": 'Internal Server Error'
        }), 500

    @app.errorhandler(400)
    def bad_request(error):
        print(error)
        return jsonify({
        "success": False,
        "error": 400,
        "message": 'Bad Request'
        }), 400

    @app.errorhandler(405)
    def method_not_allowed(error):
        print(error)
        return jsonify({
        "success": False,
        "error": 405,
        "message": 'Method Not Allowed'
        }), 405

    return app

app = create_app()

#if __name__ == '__main__':
    #APP.run(host='0.0.0.0', port=8080, debug=True)

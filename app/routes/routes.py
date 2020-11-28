import os
from flask import Blueprint, request, jsonify, abort, redirect, render_template
from flask import json
from ..models.models import Actor, Movie
from ..auth.auth import requires_auth, AUTH0_DOMAIN, ALGORITHMS, API_AUDIENCE

CLIENT_ID = os.environ["CLIENT_ID"]
CALLBACK_URL = os.environ["CALLBACK_URL"]
routes_blueprint = Blueprint("routes_blueprint", __name__, template_folder="templates")


@routes_blueprint.route("/status", methods=["GET"])
def status():
    message = {"healthy": True}
    return jsonify(message)


@routes_blueprint.route("/auth", methods=["GET"])
def auth_url():
    url = f"https://{AUTH0_DOMAIN}/authorize?audience={API_AUDIENCE}&response_type=token&client_id={CLIENT_ID}&redirect_uri={CALLBACK_URL}"
    return redirect(url)


@routes_blueprint.route("/token", methods=["GET"])
def get_token():
    url = request.url
    return render_template("index.html")


@routes_blueprint.route("/actors", methods=["GET"])
@requires_auth(permission="get:actors")
def show_actors(payload):
    actors = Actor.query.all()
    if len(actors) == 0:
        abort(404)
    else:
        actors = [a.format() for a in actors]
        response = {"count": len(actors), "success": True, "actors": actors}
        return jsonify(response)


@routes_blueprint.route("/movies", methods=["GET"])
@requires_auth(permission="get:movies")
def show_movies(payload):
    movies = Movie.query.all()
    if len(movies) == 0:
        abort(404)
    else:
        movies = [m.format() for m in movies]
        response = {"count": len(movies), "success": True, "movies": movies}
        return jsonify(response)


@routes_blueprint.route("/actors/<int:id>", methods=["DELETE"])
@requires_auth(permission="delete:actors")
def remove_actor(payload, id):
    try:
        actor = Actor.query.filter_by(id=id).one_or_none()
    except:
        abort(404)
    if actor is None:
        abort(404)
    else:
        try:
            actor.delete()
            response = {"success": True, "deleted": id}
            return jsonify(response)
        except:
            abort(422)


@routes_blueprint.route("/movies/<int:id>", methods=["DELETE"])
@requires_auth(permission="delete:movies")
def remove_movie(payload, id):
    try:
        movie = Movie.query.filter_by(id=id).one_or_none()
    except:
        abort(404)
    if movie is None:
        abort(404)
    else:
        try:
            movie.delete()
            response = {"success": True, "deleted": id}
            return jsonify(response)
        except:
            abort(422)


@routes_blueprint.route("/actors", methods=["POST"])
@requires_auth(permission="post:actors")
def add_actor(payload):
    data = request.get_json()
    if ("name" in data) and ("age" in data) and ("gender" in data):
        name = data["name"].lower()
        age = data["age"]
        gender = data["gender"].lower()
        if gender not in ["male", "female"]:
            abort(400)
        actor = Actor(name, age, gender)
        try:
            actor.insert()
            resp = {"success": True, "created": actor.id}
            return jsonify(resp)
        except:
            abort(422)
    else:
        abort(400)


@routes_blueprint.route("/movies", methods=["POST"])
@requires_auth(permission="post:movies")
def add_movie(payload):
    data = request.get_json()
    if ("title" in data) and ("release_date" in data):
        title = data["title"].lower()
        release_date = data["release_date"]
        movie = Movie(title, release_date)
        try:
            movie.insert()
            resp = {"success": True, "created": movie.id}
            return jsonify(resp)
        except:
            abort(422)
    else:
        abort(400)


@routes_blueprint.route("/actors/<int:id>", methods=["PATCH"])
@requires_auth(permission="patch:actors")
def update_actor(payload, id):
    actor = Actor.query.filter_by(id=id).one_or_none()
    if actor is None:
        abort(404)
    else:
        data = request.get_json()
        if ("name" in data) or ("age" in data) or ("gender" in data):
            name = data.get("name", None)
            age = data.get("age", None)
            gender = data.get("gender", None)
            if name is not None:
                actor.name = name
            if age is not None:
                actor.age = age
            if gender is not None:
                actor.gender = gender
            try:
                actor.update()
                resp = {"success": True, "updated": id}
                return jsonify(resp)
            except:
                abort(422)
        else:
            abort(400)


@routes_blueprint.route("/movies/<int:id>", methods=["PATCH"])
@requires_auth(permission="patch:movies")
def update_movie(payload, id):
    movie = Movie.query.filter_by(id=id).one_or_none()
    if movie is None:
        abort(404)
    else:
        data = request.get_json()
        if ("title" in data) or ("release_date" in data):
            title = data.get("title", None)
            release_date = data.get("release_date", None)
            if title is not None:
                movie.title = title
            if release_date is not None:
                movie.release_date = release_date
            try:
                movie.update()
                resp = {"success": True, "updated": id}
                return jsonify(resp)
            except:
                abort(422)
        else:
            abort(400)

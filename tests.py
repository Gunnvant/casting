import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy


from app import create_app
from app.models.models import Actor, Movie, setup_db, db_drop_and_create_all
from config import bearer_tokens

"""
Create dict with Authorization key and Bearer
token as values.
Later used by test classes as Header
"""

casting_assistant_auth_header = {
    "Authorization": bearer_tokens["casting_assistant"]
}

casting_director_auth_header = {
    "Authorization": bearer_tokens["casting_director"]
}

executive_producer_auth_header = {
    "Authorization": bearer_tokens["executive_producer"]
}


class CastingTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = os.environ["DATABASE_URL"]
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    Tests for checking the endpoints with Executive
    roducer role, this role can access all the endpoints
    """

    def test_get_actors(self):
        """This tests the GET/actors endpoint"""
        # Create some data in the db
        actor = Actor(name="xyz", age=32, gender="male")
        actor.insert()
        id = actor.id

        # Hit the GET/actors endpoint
        res = self.client().get("/api/actors",
                                headers=executive_producer_auth_header)
        data = json.loads(res.data)

        # Check data and keys returned
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["count"], 1)
        self.assertIsNotNone(data["actors"])

        # Delete the actor from db
        actor = Actor.query.filter_by(id=id).one_or_none()
        actor.delete()

    def test_get_actors_failure(self):
        """This tests the endpoint when no actors exist in database"""
        res = self.client().get("/api/actors",
                                headers=executive_producer_auth_header)
        data = json.loads(res.data)

        # Check data and keys returned
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)

    def test_get_movies(self):
        """This tests the GET/movies endpoint"""

        # Crete a row in movies table
        movie = Movie(title="xyz", release_date="26/11/2021")
        movie.insert()
        id = movie.id

        # Hit GET/movies endpoint
        res = self.client().get("/api/movies",
                                headers=executive_producer_auth_header)
        data = json.loads(res.data)

        # Check data and keys returned
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["count"], 1)
        self.assertIsNotNone(data["movies"])

        # Delete the movies object
        movie = Movie.query.filter_by(id=id).one_or_none()
        movie.delete()

    def test_get_movies_failure(self):
        '''Tests the GET/movies when there is no data in db'''

        res = self.client().get("/api/movies",
                                headers=executive_producer_auth_header)
        data = json.loads(res.data)

        # Check data and keys returned
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)

    def test_delete_actors(self):
        """Tests the DELETE/actors when actor exists in db"""

        # Create an actor resource in db
        actor = Actor(name="xyz", age=29, gender="male")
        actor.insert()
        id = actor.id

        # Hit DELETE/actor/id endpoint
        res = self.client().delete(
            f"/api/actors/{id}", headers=executive_producer_auth_header
        )
        data = json.loads(res.data)

        # Check the data and keys returned
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["deleted"], id)

        # Check if the actor was removed from db
        actor = Actor.query.filter_by(id=id).one_or_none()
        self.assertIsNone(actor)

    def test_delete_actor_failure(self):
        """Tests the endpoint when invalid id is provided"""

        id = "bfkl"

        # Hit the DELETE/actor/id endpoint
        res = self.client().delete(
            f"/api/actors/{id}", headers=executive_producer_auth_header
        )
        data = json.loads(res.data)

        # Check the data and keys returned
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)

    def test_delete_movies(self):
        """Tests the endpoint when movies exist in db"""

        # Create a movie resource
        movie = Movie(title="xyz", release_date="26/11/2021")
        movie.insert()
        id = movie.id

        # Hit DELETE/movie/id endpoint
        res = self.client().delete(
            f"/api/movies/{id}", headers=executive_producer_auth_header
        )
        data = json.loads(res.data)

        # Check the data and keys returned
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["deleted"], id)

        # Check if movie has been removed from db
        movie = Movie.query.filter_by(id=id).one_or_none()
        self.assertIsNone(movie)

    def test_delete_movies_failure(self):
        """Test DELETE/movies when incorrect id is provided"""

        id = "asdk"

        # Hit DELETE/movies/id endpoint
        res = self.client().delete(
            f"/api/movies/{id}", headers=executive_producer_auth_header
        )
        data = json.loads(res.data)

        # Check the data and keys returned
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)

    def test_post_actors(self):
        """This tests the response when correct data is sent"""

        payload = {"name": "xyz", "age": 34, "gender": "male"}
        res = self.client().post(
            "/api/actors", json=payload, headers=executive_producer_auth_header
        )
        data = json.loads(res.data)

        # Check the data and the keys returned
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        # Check if the actor persisted in data
        actor = Actor.query.filter_by(id=data["created"]).one_or_none()
        self.assertIsNotNone(actor)
        # Delete the actor
        actor.delete()

    def test_post_actors_failure(self):
        """This tests the behaviour when post data has bad keys"""
        payload = {"name": "xyz", "age": 29}

        # Hit the endpoint
        res = self.client().post(
            "/api/actors", json=payload, headers=executive_producer_auth_header
        )
        data = json.loads(res.data)

        # Check the data and keys sent
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)

    def test_post_movies(self):
        """This tests the response when correct data is sent"""
        payload = {"title": "xyz", "release_date": "26/11/2021"}

        # Hit the endpoint
        res = self.client().post(
            "/api/movies", json=payload, headers=executive_producer_auth_header
        )
        data = json.loads(res.data)

        # Check the data and keys sent
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

        # Check if the data persisted in db
        movie = Movie.query.filter_by(id=data["created"]).one_or_none()
        self.assertIsNotNone(movie)

        # Remove the movie from db
        movie.delete()

    def test_post_movies_failure(self):
        """Tests when keys are missing in post request"""
        payload = {"title": "xyz"}

        # Hit the endpoint
        res = self.client().post(
            "/api/movies", json=payload, headers=executive_producer_auth_header
        )
        data = json.loads(res.data)

        # Check the data and keys
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)

    def test_actors_patch(self):
        """Tests the behavior when correct patch request is sent"""
        payload = {"age": 24}

        # Create an actor resource in db
        actor = Actor(name="xyz", age=32, gender="male")
        actor.insert()
        id = actor.id

        # Hit the patch endpoint
        res = self.client().patch(f"/api/actors/{id}",
                                  json=payload,
                                  headers=executive_producer_auth_header
                                  )
        data = json.loads(res.data)

        # Check the messages keys returned
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

        # Check if the data persisted
        actor = Actor.query.filter_by(id=id).one_or_none()
        self.assertEqual(actor.age, payload["age"])

        # Delete the actor resource
        actor.delete()

    def test_actors_patch_failure(self):
        """Tests the behaviour when wrong id is sent"""
        payload = {"age": 24}
        # Create an actor resource in db
        actor = Actor(name="xyz", age=32, gender="male")
        actor.insert()
        id = actor.id

        # Hit the patch endpoint
        res = self.client().patch(
            f"/api/actors/{id+100}",
            json=payload,
            headers=executive_producer_auth_header,
        )
        data = json.loads(res.data)

        # Check the messages keys returned
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)

        # Check the data should not have presisted
        actor = Actor.query.filter_by(id=id).one_or_none()
        self.assertNotEqual(actor.age, payload["age"])

        # Delete the actor resource
        actor.delete()

    def test_actors_patch_failure_wrong_payload(self):
        """Tests if keys in the patch request are invalid"""

        payload = {"title": "xyz"}

        # Create an actor resource in db
        actor = Actor(name="xyz", age=32, gender="male")
        actor.insert()
        id = actor.id

        # Hit the patch endpoint
        res = self.client().patch(f"/api/actors/{id}",
                                  json=payload,
                                  headers=executive_producer_auth_header
                                  )
        data = json.loads(res.data)

        # Check the messages keys returned
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)

        # Delete the actor resource
        actor.delete()

    def test_movies_patch(self):
        """Tests the behavior when correct patch request is sent"""
        payload = {"title": "xyz"}

        # Create a Movie resource in db
        movie = Movie(title="abc", release_date="26/11/2021")
        movie.insert()
        id = movie.id

        # Hit the patch endpoint
        res = self.client().patch(f"/api/movies/{id}",
                                  json=payload,
                                  headers=executive_producer_auth_header
                                  )
        data = json.loads(res.data)

        # Check the messages keys returned
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

        # Check if the data persisted
        movie = Movie.query.filter_by(id=id).one_or_none()
        self.assertEqual(movie.title, payload["title"])

        # Delete the movie resource
        movie.delete()

    def test_movies_patch_failure(self):
        """Tests the behaviour when wrong id is sent"""
        payload = {"title": "xyz"}
        # Create an movie resource in db
        movie = Movie(title="abc", release_date="26/11/2021")
        movie.insert()
        id = movie.id

        # Hit the patch endpoint
        res = self.client().patch(
            f"/api/movies/{id+100}",
            json=payload,
            headers=executive_producer_auth_header,
        )
        data = json.loads(res.data)

        # Check the messages keys returned
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)

        # Check the data should not have presisted
        movie = Movie.query.filter_by(id=id).one_or_none()
        self.assertNotEqual(movie.title, payload["title"])

        # Delete the actor resource
        movie.delete()

    def test_movies_patch_failure_wrong_payload(self):
        """Tests if keys in the patch request are invalid"""

        payload = {"age": 20}

        # Create an actor resource in db
        movie = Movie(title="xyz", release_date="26/11/2021")
        movie.insert()
        id = movie.id

        # Hit the patch endpoint
        res = self.client().patch(f"/api/movies/{id}",
                                  json=payload,
                                  headers=executive_producer_auth_header
                                  )
        data = json.loads(res.data)

        # Check the messages keys returned
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)

        # Delete the actor resource
        movie.delete()

    """
    Tests for Casting Director, this
    role doesn't have access to /POST/movies
    """

    def test_casting_director_get_movies(self):
        """This tests the GET/actors endpoint"""
        # Create some data in the db
        actor = Actor(name="xyz", age=32, gender="male")
        actor.insert()
        id = actor.id

        # Hit the GET/actors endpoint
        res = self.client().get("/api/actors",
                                headers=casting_director_auth_header)
        data = json.loads(res.data)

        # Check data and keys returned
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["count"], 1)
        self.assertIsNotNone(data["actors"])

        # Delete the actor from db
        actor = Actor.query.filter_by(id=id).one_or_none()
        actor.delete()

    def test_casting_director_post_movies(self):
        """This tests the response when correct data is sent"""
        payload = {"title": "xyz", "release_date": "26/11/2021"}

        # Hit the endpoint
        res = self.client().post(
            "/api/movies", json=payload, headers=casting_director_auth_header
        )
        data = json.loads(res.data)

        # Check the data and keys sent
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)

    """
    Tests for Casting Assistant Role
    """

    def test_casting_assistant_get_actors(self):
        """This tests the GET/actors endpoint"""
        # Create some data in the db
        actor = Actor(name="xyz", age=32, gender="male")
        actor.insert()
        id = actor.id

        # Hit the GET/actors endpoint
        res = self.client().get("/api/actors",
                                headers=casting_assistant_auth_header)
        data = json.loads(res.data)

        # Check data and keys returned
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["count"], 1)
        self.assertIsNotNone(data["actors"])

        # Delete the actor from db
        actor = Actor.query.filter_by(id=id).one_or_none()
        actor.delete()

    def test_casting_assistant_post_movies(self):
        """This tests the response when correct data is sent"""
        payload = {"title": "xyz", "release_date": "26/11/2021"}

        # Hit the endpoint
        res = self.client().post(
            "/api/movies", json=payload, headers=casting_assistant_auth_header
        )
        data = json.loads(res.data)

        # Check the data and keys sent
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)


if __name__ == "__main__":
    unittest.main()

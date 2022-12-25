from database import db
from config import DevelopmentConfig
from models import Game, Developer
import json
from flask import Flask, request, Response
from flask_restx import Api, Resource, fields


app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
db.init_app(app)

api = Api(
    app,
    title="Games Api Flask",
    version="1.0",
    description="Create a Games and Developers base.",
    doc="/docs",
)

ns_games = api.namespace("games", description="Games Operations")
game_swagger = api.model(
    "Game",
    {
        "game_title": fields.String(required=True, description="The game title"),
        "year": fields.Integer(
            required=True, description="The year of release of the game"
        ),
        "developer_name": fields.String(
            required=True, description="The game developer"
        ),
    },
)

ns_developers = api.namespace("developers", description="Developers Operations")
dev_swagger = api.model(
    "Developer",
    {
        "developer_name": fields.String(
            required=True, description="The game developer"
        ),
    },
)

with app.app_context():
    db.create_all()


@api.route("/games", endpoint="games")
class GamesEndpoint(Resource):
    @ns_games.marshal_list_with(game_swagger)
    def get(self):
        """Get all games"""
        games = Game.query.all()
        return [game.json() for game in games]

    @ns_games.expect(game_swagger)
    @ns_games.response(201, "Created")
    def post(self):
        """Create a new game"""
        record = json.loads(request.data)
        game = Game(**record)
        db.session.add(game)
        db.session.commit()
        return Response(status=201)


@api.route("/games/<int:id>")
class GameEndpoint(Resource):
    @ns_games.marshal_with(game_swagger)
    def get(self, id):
        """Get a game"""
        game = Game.query.filter_by(id=id).first_or_404(
            description="There is no game with id {}".format(id)
        )
        return game.json()

    @ns_games.expect(game_swagger)
    def put(self, id):
        """Update a game"""
        Game.query.filter_by(id=id).first_or_404(
            description="There is no game with id {}".format(id)
        )
        record = json.loads(request.data)
        Game.query.filter_by(id=id).update(record)
        db.session.commit()
        return Response(status=204)

    @ns_games.response(204, "No content")
    def delete(self, id):
        """Delete a game"""
        game = Game.query.filter_by(id=id).first_or_404(
            description="There is no game with id {}".format(id)
        )
        db.session.delete(game)
        db.session.commit()
        return Response(status=204)


@api.route("/developers")
class DevelopersEndpoint(Resource):
    @ns_developers.marshal_list_with(dev_swagger)
    def get(self):
        """Get all developers"""
        developers = Developer.query.all()
        return [dev.json() for dev in developers]

    @ns_developers.expect(dev_swagger)
    @ns_games.response(201, "Created")
    def post(self):
        """Create a new developer"""
        record = json.loads(request.data)
        developer = Developer(**record)
        db.session.add(developer)
        db.session.commit()
        return Response(status=201)


@api.route("/developers/<string:name>")
class DeveloperEndpoint(Resource):
    @ns_developers.marshal_with(dev_swagger)
    def get(self, name):
        """Get a developer"""
        name = name.title()
        developer = Developer.query.filter_by(developer_name=name).first_or_404(
            description="There is no developer with name {}".format(name)
        )
        return developer.json()

    @ns_developers.expect(dev_swagger)
    @ns_games.response(204, "No content")
    def put(self, name):
        """Update a developer"""
        name = name.title()
        Developer.query.filter_by(developer_name=name).first_or_404(
            description="There is no developer with name {}".format(name)
        )
        record = json.loads(request.data)
        Developer.query.filter_by(developer_name=name).update(record)
        db.session.commit()
        return Response(status=204)

    @ns_games.response(204, "No content")
    def delete(self, name):
        """Delete a developer"""
        name = name.title()
        developer = Developer.query.filter_by(developer_name=name).first_or_404(
            description="There is no developer with name {}".format(name)
        )
        db.session.delete(developer)
        db.session.commit()
        return Response(status=204)

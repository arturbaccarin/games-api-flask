import pytest
from database import db
from config import TestingConfig
from app import app
from models import Game, Developer
import json


@pytest.fixture(scope="module")
def test_client():
    app.config.from_object(TestingConfig)
    db.init_app(app)
    with app.test_client() as test_client:
        with app.app_context():
            yield test_client


@pytest.fixture(scope="module")
def init_database():
    db.create_all()
    developer1 = Developer("Criterion")
    developer2 = Developer("Namco")
    db.session.add(developer1)
    db.session.add(developer2)

    game1 = Game("Burnout 3", 2004, "Criterion")
    game2 = Game("Tekken 7", 2015, "Namco")
    db.session.add(game1)
    db.session.add(game2)

    db.session.commit()

    yield
    db.drop_all()


# Games
def test_get_games(test_client, init_database):
    response = test_client.get("/games")
    response_data = json.loads(response.data.decode("utf-8"))
    assert response.status_code == 200
    assert len(response_data) == 2
    assert response_data[0]["game_title"] == "Burnout 3"


def test_get_game(test_client, init_database):
    response = test_client.get("/games/2")
    response_data = json.loads(response.data.decode("utf-8"))
    assert response.status_code == 200
    assert response_data["game_title"] == "Tekken 7"


def test_post_game(test_client, init_database):
    response = test_client.post(
        "/games",
        data=json.dumps(
            {"game_title": "Overwatch 2", "year": "2022", "developer_name": "Blizzard"}
        ),
    )
    assert response.status_code == 201
    response = test_client.get("/games/3")
    response_data = json.loads(response.data.decode("utf-8"))
    assert response_data["game_title"] == "Overwatch 2"


def test_put_game(test_client, init_database):
    response = test_client.put(
        "/games/1",
        data=json.dumps(
            {
                "game_title": "Halo: Combat Evolved",
                "year": "2001",
                "developer_name": "Microsoft",
            }
        ),
    )
    assert response.status_code == 204
    assert response.data == b""
    response = test_client.get("/games/1")
    response_data = json.loads(response.data.decode("utf-8"))
    assert response_data["game_title"] == "Halo: Combat Evolved"


def test_delete_game(test_client, init_database):
    response = test_client.delete("/games/1")
    assert response.status_code == 204
    assert response.data == b""
    response = test_client.get("/games")
    assert not b"Burnout 3" in response.data


# Developers
def test_get_developers(test_client, init_database):
    response = test_client.get("/developers")
    response_data = json.loads(response.data.decode("utf-8"))
    assert response.status_code == 200
    assert len(response_data) == 2
    assert response_data[0]["developer_name"] == "Criterion"


def test_get_developer(test_client, init_database):
    response = test_client.get("/developers/namco")
    response_data = json.loads(response.data.decode("utf-8"))
    assert response.status_code == 200
    assert response_data["developer_name"] == "Namco"


def test_post_developer(test_client, init_database):
    response = test_client.post(
        "/developers",
        data=json.dumps(
            {
                "developer_name": "Microsoft",
            }
        ),
    )
    assert response.status_code == 201
    response = test_client.get("/developers/microsoft")
    response_data = json.loads(response.data.decode("utf-8"))
    assert response_data["developer_name"] == "Microsoft"


def test_put_developer(test_client, init_database):
    response = test_client.put(
        "/developers/criterion",
        data=json.dumps(
            {
                "developer_name": "Nintendo",
            }
        ),
    )
    assert response.status_code == 204
    assert response.data == b""
    response = test_client.get("/developers/nintendo")
    response_data = json.loads(response.data.decode("utf-8"))
    assert response_data["developer_name"] == "Nintendo"


def test_delete_developer(test_client, init_database):
    response = test_client.delete("/developers/namco")
    assert response.status_code == 204
    assert response.data == b""
    response = test_client.get("/developers")
    assert not b"Namco" in response.data

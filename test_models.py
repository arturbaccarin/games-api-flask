from models import Game, Developer


def test_new_game():
    game = Game("Twisted Metal 2", 1996, "Sony")
    assert game.game_title == "Twisted Metal 2"
    assert game.year == 1996
    assert game.developer_name == "Sony"
    assert str(game) == "<Game 'Twisted Metal 2'>"


def test_new_developer():
    developer = Developer("Nintendo")
    assert developer.developer_name == "Nintendo"
    assert str(developer) == "<Developer 'Nintendo'>"

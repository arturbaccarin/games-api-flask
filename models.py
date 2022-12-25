from database import db


class Game(db.Model):
    __tablename__ = "games"
    id = db.Column(db.Integer, primary_key=True)
    game_title = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    developer_name = db.Column(
        db.String(100), db.ForeignKey("developers.developer_name"), nullable=False
    )

    def __init__(self, game_title, year, developer_name):
        self.game_title = game_title
        self.year = year
        self.developer_name = developer_name

    def __repr__(self):
        return "<Game %r>" % self.game_title

    def json(self):
        return {
            "id": self.id,
            "game_title": self.game_title,
            "year": self.year,
            "developer_name": self.developer_name,
        }


class Developer(db.Model):
    __tablename__ = "developers"
    developer_name = db.Column(db.String(100), primary_key=True)
    games = db.relationship("Game", backref="developers", cascade="all,delete")

    def __init__(self, developer_name):
        self.developer_name = developer_name.title()

    def __repr__(self):
        return "<Developer %r>" % self.developer_name

    def json(self):
        return {
            "developer_name": self.developer_name,
            "games": [game.json() for game in self.games],
        }

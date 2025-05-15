import json


class Title:
    def __init__(self, row, rating=None):
        self.id = row[0]
        self.title = row[1]
        self.start_year = row[2]
        self.end_year = row[3]
        self.runtime = row[4]
        self.type = row[5]
        self.rating = rating

    def __str__(self):
        attrs = vars(self)
        return ', '.join("%s: %s" % item for item in attrs.items())

    def __repr__(self):
        return str(self)


class Character:
    def __init__(self, id, name, character):
        self.id = id
        self.name = name
        self.character = character

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f"{self.name} as {self.character}"

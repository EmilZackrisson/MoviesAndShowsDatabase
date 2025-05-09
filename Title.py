class Title:
    def __init__(self, id: str, title: str, rating: float):
        self.id = id
        self.title = title
        self.rating = rating

    def __str__(self):
        return ''.join(str(item) for item in self)

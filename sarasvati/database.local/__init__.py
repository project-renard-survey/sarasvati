from api.models import Thought
from api.plugins import DatabasePlugin


class LocalDatabasePlugin(DatabasePlugin):
    def __init__(self):
        super().__init__()
        self.__cache = []

    def create(self):
        t = Thought()
        self.__cache.append(t)
        return t

    def delete(self, thought):
        self.__cache.remove(thought)

    def find(self, query):
        if query is None:
            return self.__cache.copy()
        for t in self.__cache:
            if t.title == query:
                return t

    def get(self, query):
        result = self.find(query)
        if not result:
            raise Exception("Nothing found")
        return result

from PyQt5.QtCore import QObject, pyqtSignal, QVariant, pyqtSlot

from sarasvati import get_api
from sarasvati.event import Event
from ..plex import Plex


class PlexController(QObject):
    __command = pyqtSignal(QVariant, arguments=['command'], name="command")

    def __init__(self):
        QObject.__init__(self)
        self.__plex = Plex()

        self.changed = Event()

        # subscribe for events
        e = get_api().events
        e.activated.subscribe(self.__on_activated)
        e.changing.subscribe(self.__on_changing)
        e.changed.subscribe(self.__on_changed)
        e.created.subscribe(self.__on_brain_changed)
        e.deleted.subscribe(self.__on_brain_changed)

    @property
    def plex(self):
        return self.__plex

    def __update(self, thought):
        if thought is None:
            return
        state, actions = self.__plex.activate(thought, True)
        self.changed.notify(state, actions)

        for cmd in actions:
            v = {"cmd": cmd.name, "key": cmd.thought.key}

            if cmd.name == "add":
                v["title"] = cmd.thought.title
                v["x"] = cmd.data["pos"][0]
                v["y"] = cmd.data["pos"][1]
            if cmd.name == "move":  # or cmd.name == "set_pos_to":
                v["x"] = cmd.data[0]
                v["y"] = cmd.data[1]
            self.__command.emit(QVariant(v))

        if thought:
            for links in thought.links.all:
                self.__command.emit({"cmd": "link", "from": thought.key, "to": links.key,
                                     "ft": thought.title, "tt": links.title})

    @pyqtSlot(int, int, name="on_resize")
    def __on_resize(self, width, height):
        """On application window resize"""
        self.__plex.layout.set_size(width, height)
        self.__update(self.__plex.thought)

    def __on_activated(self, thought):
        """On thought activated"""
        self.__update(thought)

    def __on_changed(self, thought):
        """On thought changing"""
        self.__command.emit({"cmd": "change", "key": thought.key, "title": thought.title})
        self.__update(self.__plex.thought)

    def __on_changing(self, thought, data):
        """On thought changing"""
        self.command.emit({
            "cmd": "change", "key": thought.key,
            "title": data["title"]
        })

    def __on_brain_changed(self, thought):
        """On brain changed"""
        self.__update(self.__plex.thought)

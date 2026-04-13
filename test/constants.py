from enum import Enum

class Route(str,Enum):
    HOST = "overleaf.com"
    MAIN= "https://www.overleaf.com/"
    PROJECT ="project"
    SOCKETIO = "socket.io/1/"
    WEBSOCKET="websocket/"
    DOWNLOAD="/download/zip"
    def __str__(self):
        return self.value
class Locations(str,Enum):
    RESPONSE= "data/response/"
    def __str__(self):
        return self.value


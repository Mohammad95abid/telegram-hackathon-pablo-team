

class DBException(Exception):

    def __init__(self, message):
        if message:
            self.message = message
        else:
            self.message = "DBException Occurred."


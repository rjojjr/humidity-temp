class GenericResponse:

    def __init__(self, message, statusCode, status):
        self.message = message
        self.statusCode = statusCode
        self.status = status

class UnauthedResponse:

    def __init__(self, message):
        self.message = message
        self.statusCode = 401
        self.status = "Unauthorized"
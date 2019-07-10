from rest_framework.response import Response


class LogicException(BaseException):
    def __init__(self, message):
        self.message = message

    def get_web_response(self):
        return Response({'res': '', 'error': self.message})

import abc
from logging import Handler

from requests import Response


class ResponseHandler(Handler, abc.ABC):
    def handle(self, res: Response):
        pass
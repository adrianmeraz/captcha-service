import typing

from . import exceptions, logs

logger = logs.logger


class APIGatewayRouter:
    """
    Small router for parsing API Gateway Events and calling the matching lambda
    Based on ideas from Tiny-Router
    https://kevinquinn.fun/blog/tiny-python-router-for-aws-lambda/
    """
    VALID_METHODS = ['GET', 'POST', 'PUT', 'DELETE']

    def __init__(self):
        self._route_map = dict()

    def add_route(self, func: typing.Callable, http_method: str, path: str):
        if self._route_map[http_method][path]:
            raise exceptions.RouteAlreadyExists(method=http_method, path=path)
        self._route_map[http_method][path] = func

    def handle_event(self, http_method: str, path: str, *args, **kwargs):
        logger.info(f'routing event -> http_method: {http_method}, path: {path}')
        try:
            return self._route_map[http_method][path](*args, **kwargs)
        except KeyError:
            raise exceptions.RouteNotFound(http_method, path)

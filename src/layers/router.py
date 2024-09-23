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

    @property
    def routes(self) -> dict:
        return self._route_map

    def add_route(self, fn: typing.Callable, http_method: str, path: str):
        if http_method not in self.VALID_METHODS:
            raise exceptions.InvalidHttpMethod(http_method=http_method, valid_methods=self.VALID_METHODS)
        if http_method in self._route_map and path in self._route_map[http_method]:
            raise exceptions.RouteAlreadyExists(method=http_method, path=path)
        if http_method not in self._route_map:
            self._route_map[http_method] = dict()
        self._route_map[http_method][path] = fn
        logger.info(f'Added route to router -> http_method: {http_method}, path: {path}')

    def handle_event(self, http_method: str, path: str, *args, **kwargs):
        logger.info(f'Routing event -> http_method: {http_method}, path: {path}')
        try:
            return self._route_map[http_method][path](*args, **kwargs)
        except KeyError:
            raise exceptions.RouteNotFound(http_method=http_method, path=path)

import random
from abc import ABC, abstractmethod

from . import const


class ProxyInterface(ABC):
    @classmethod
    @abstractmethod
    def get_proxy_url(cls, **kwargs) -> str:
        pass

    @classmethod
    def get_weighted_country(cls):
        countries, weights = zip(const.PROXY_COUNTRY_WEIGHTS)
        return random.choices(population=countries, weights=weights, k=1)[0]

from enum import Enum


class EventStatus(str, Enum):
    INIT = 'INIT'
    ACCEPTED = 'ACCEPTED'
    REJECTED = 'REJECTED'

# class taken from the site:
# https://refactoring.guru/design-patterns/singleton/python/example

from typing import Any


class SingletonMeta(type):
    _instances = dict[type, object]()

    def __call__(cls, *args: Any, **kwargs: Any):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

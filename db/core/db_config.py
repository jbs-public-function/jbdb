import os
import settings


class DBConfig(object):
    __slots__ = ['driver', 'user_name', 'password', 'host', 'port', 'db_name']
    uri = '{driver}://{user_name}:{password}@{host}:{port}/{db_name}'

    def __init__(self, **config):
        for slot in self.__slots__:
            if hasattr(self, slot):
                continue
            setattr(self, slot, os.environ.get(slot.upper()))
        for key, value in config.items():
            setattr(self, key, value)
        self.validate_attributes(self)
    
    @property
    def connect_string(self):
        return self.uri.format(**{slot: getattr(self, slot) for slot in self.__slots__})

    @classmethod
    def validate_attributes(cls, config_obj):
        if any([getattr(config_obj, slot) == None for slot in cls.__slots__]):
            raise DBConfigValueError(f"{', '.join([slot for slot in cls.__slots__ if getattr(config_obj, slot) is None])} cant be None")

    
    
class DBConfigValueError(ValueError):
    pass
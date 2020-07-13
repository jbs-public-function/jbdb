import os
import settings


class DBConfigBase(object):
    __slots__ = ['driver']
    db_uri = '{driver}'

    def __init__(self, **config):
        self.validate_slot_attributes(config)
        environ = {slot: os.environ.get(slot.upper()) for slot in self.__slots__}
        environ.update(config)
        for slot in self.__slots__:
            value = environ.pop(slot)
            setattr(self, slot, value)
        self.validate_slot_values(self)
    
    @property
    def connect_string(self):
        return self.db_uri.format(**{slot: getattr(self, slot) for slot in self.__slots__})

    @classmethod
    def validate_slot_values(cls, config_obj):
        invalid_slots = [slot for slot in cls.__slots__ if getattr(config_obj, slot) == None]
        if len(invalid_slots) > 0:
            invalid_slots = '\n'.join(invalid_slots)
            raise DBConfigValueError(f'The following attributes can not be None:\n{invalid_slots}')

    @classmethod
    def validate_slot_attributes(cls, config):
        missing_slots = [slot for slot in cls.__slots__ if slot not in config and slot not in os.environ]
        if len(missing_slots) > 0:
            missing_slots = '\n'.join(missing_slots)
            raise DBConfigAttributeError(f'The following attributes are required:\n{missing_slots}')

    
class DBConfigValueError(ValueError):
    pass


class DBConfigAttributeError(AttributeError):
    pass

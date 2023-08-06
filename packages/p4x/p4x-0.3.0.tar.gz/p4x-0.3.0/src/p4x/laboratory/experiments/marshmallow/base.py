from abc import abstractmethod

from marshmallow import Schema, fields, post_load

__author__ = "Philipp Tempel"
__email__ = "p.tempel@tudelft.nl"


class BaseSchema(Schema):
    name = fields.String()
    path = fields.String()

    class Meta:
        ordered = True

    @property
    @abstractmethod
    def __model__(self):
        raise NotImplementedError()

    @post_load
    def make_object(self, data, **kwargs):
        return self.__model__(**data)


__all__ = [
        'BaseSchema',
]

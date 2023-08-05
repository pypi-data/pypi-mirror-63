from .base import Base
from typing import Set

import attr
from marshmallow_annotations.ext.attrs import AttrsSchema


@attr.s(auto_attribs=True, kw_only=True)
class Badge(Base):
    """
    This represents a badge object
    """
    tag_name: str
    tag_type: str = 'badge'

    def __init__(self, tag_name: str):
        self.tag_name = tag_name
        self.tag_type = 'badge'

    @classmethod
    def get_attrs(cls) -> Set:
        return {
            'tag_name',
            'tag_type'
        }

    @staticmethod
    def get_type() -> str:
        return 'badge'

    def get_id(self) -> str:
        # this isn't actually an ES document
        return ''

    def __repr__(self) -> str:
        return 'Badge({!r}, {!r})'.format(self.tag_name, self.tag_type)


class BadgeSchema(AttrsSchema):
    class Meta:
        target = Badge
        register_as_scheme = True

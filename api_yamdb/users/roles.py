from enum import Enum


class UserRoles(Enum):
    """Перечисление для выбора ролей."""

    user = 'user'
    moderator = 'moderator'
    admin = 'admin'

    @classmethod
    def choices(cls):
        return tuple((attribute.name, attribute.value) for attribute in cls)

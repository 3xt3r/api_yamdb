from rest_framework import serializers

ME_ERROR = {
    'error': 'Использовать имя me запрещено.'
}


def username_not_me(value):

    me = {'ME', 'me', 'Me', 'mE'}
    if value in me:
        raise serializers.ValidationError(ME_ERROR)

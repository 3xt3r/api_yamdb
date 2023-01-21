from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.validators import UnicodeUsernameValidator
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User
from django.shortcuts import get_object_or_404
from .validators import username_not_me

username_validator = UnicodeUsernameValidator()

ME_ERROR = {
    'error': 'Использовать имя me запрещено.'
}

DOUBLE_REVIEW_ERROR = {
    'error': 'Невозможно оставить два отзыва'
}


class GetAllUserSerializer(serializers.ModelSerializer):
    """Сериализатор модели User."""

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )

    def validate_username(self, username):
        if username in 'me':
            raise serializers.ValidationError(ME_ERROR)
        return username


class RegistrationSerializer(serializers.ModelSerializer):
    """Сериализатор для создания объекта класса User."""

    username = serializers.CharField(
        max_length=100,
        required=True,
        validators=[
            username_not_me,
            username_validator,
            UniqueValidator(queryset=User.objects.all(),
                            )
        ]
    )

    class Meta:
        model = User
        fields = ('email', 'username')
        extra_kwargs = {
            'email': {'required': True}
        }


class GetTokenSerializer(serializers.ModelSerializer):
    """Сериализатор для объекта класса User при получении токена."""

    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(
        max_length=150,
        required=True
    )

    class Meta:
        model = User
        fields = (
            'username',
            'confirmation_code'
        )


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для модели Category."""

    class Meta:
        exclude = ('id', )
        model = Category
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Genre."""

    class Meta:
        exclude = ('id', )
        model = Genre
        lookup_field = 'slug'


class TitleReadSerializer(serializers.ModelSerializer):
    """Сериализатор объектов класса Title при GET-запросе."""

    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField(read_only=True, required=False)

    class Meta:
        fields = '__all__'
        model = Title


class TitleWriteSerializer(TitleReadSerializer):
    """Сериализатор объектов класса Title при небезопасных запросах."""

    genre = serializers.SlugRelatedField(queryset=Genre.objects.all(),
                                         slug_field='slug',
                                         many=True)
    category = serializers.SlugRelatedField(queryset=Category.objects.all(),
                                            slug_field='slug',
                                            )


class CurrentReviewDefault:
    requires_context = True

    def __call__(self, serializer_field):
        review_id = serializer_field.context['view'].kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        return review


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор объектов класса Comment."""

    author = serializers.SlugRelatedField(
        read_only=True, required=False, slug_field='username')
    review = serializers.HiddenField(default=CurrentReviewDefault())

    class Meta:
        model = Comment
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор модели Review."""

    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Review
        fields = (
            'id', 'text', 'author', 'score', 'pub_date')

    def validate(self, data):
        if not self.context.get('request').method == 'POST':
            return data
        author = self.context.get('request').user
        title_id = self.context.get('view').kwargs.get('title_id')
        if Review.objects.filter(author=author, title=title_id).exists():
            raise serializers.ValidationError(
                DOUBLE_REVIEW_ERROR
            )
        return data

from django.conf import settings
from users.roles import UserRoles
from django.core.mail import send_mail
from django.db.models.aggregates import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, views, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist


from reviews.models import Category, Genre, Review, Title
from reviews.models import User
from .filters import TitleFilter
from .mixins import CustomViewSet
from .permissions import IsAdmin, ReviewCommentPermissions, AnonimReadOnly
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, GetAllUserSerializer,
                          GetTokenSerializer, RegistrationSerializer,
                          ReviewSerializer, TitleReadSerializer,
                          TitleWriteSerializer)

CODE_ERROR = {
    'Error': 'Неверный код подтвреждения.'
}

USERNAME_NOT_FOUND = {
    'Error': 'Данный пользователь не найден.'
}


class GetAllUserViewSet(viewsets.ModelViewSet):
    """Вьюсет для обьектов модели User."""

    permission_classes = [IsAdmin]
    queryset = User.objects.all()
    serializer_class = GetAllUserSerializer
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter, )
    search_fields = ('username',)

    @action(
        detail=False, methods=['GET', 'PATCH', 'PUT'],
        permission_classes=[IsAuthenticated],
        serializer_class=GetAllUserSerializer,
        url_path='me',
        url_name='me',
    )
    def me(self, request):
        user = self.request.user
        if request.method == 'PATCH':
            if ((request.data.get('role') == UserRoles.admin.name)
                    and (self.request.user.role == UserRoles.user.name)):
                data = dict(request.data)
                data['role'] = UserRoles.user.name
            else:
                data = request.data
            serializer = self.get_serializer(
                user, data=data, partial=True
            )

            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().update(request, *args, **kwargs)


class RegistrationView(views.APIView):
    """Вьюсет для создания обьектов класса User."""

    permission_classes = [AllowAny]

    @staticmethod
    def send_reg_mail(email, user):
        send_mail(
            subject='Код подтверждения для получения токена.',
            message=f'Ваш код: {user.confirmation_code}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
        )

    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')

        try:
            user = User.objects.get(username=username, email=email)
            self.send_reg_mail(email, user)
            return Response("Код на почте", status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            user = None

        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        serializer.save(email=email)
        user = get_object_or_404(
            User,
            username=serializer.validated_data.get('username'))

        self.send_reg_mail(email, user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetTokenView(views.APIView):
    """Вьюсет для получения пользователем токена."""

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = GetTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        confirmation_code = serializer.validated_data.get('confirmation_code')
        username = serializer.validated_data.get('username')
        user = get_object_or_404(User, username=username)
        if user.confirmation_code != confirmation_code:
            return Response(
                CODE_ERROR,
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(self.token(user), status=status.HTTP_200_OK)


class CategoryViewSet(CustomViewSet):
    """Вьюсет для для создания обьектов класса Category."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AnonimReadOnly | IsAdmin,)
    pagination_class = PageNumberPagination
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name',)


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для для создания обьектов класса Review."""

    serializer_class = ReviewSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        ReviewCommentPermissions
    )
    pagination_class = PageNumberPagination

    def get_title(self):
        title_id = self.kwargs.get('title_id')
        return get_object_or_404(Title, pk=title_id)

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=self.get_title()
        )


class GenreViewSet(CustomViewSet):
    """Вьюсет для для создания обьектов класса Genre."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (AnonimReadOnly | IsAdmin,)
    pagination_class = PageNumberPagination
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для для создания обьектов класса Title."""

    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')).all()
    permission_classes = (AnonimReadOnly | IsAdmin,)
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PATCH']:
            return TitleWriteSerializer
        return TitleReadSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для для создания обьектов класса Comment."""

    serializer_class = CommentSerializer
    permission_classes = [ReviewCommentPermissions, ]
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        return review.comments.all()

    def get_review(self):
        review_id = self.kwargs.get('review_id')
        return get_object_or_404(Review, pk=review_id)

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    TitleViewSet,
    CategoryViewSet,
    CommentViewSet,
    GenreViewSet,
    GetAllUserViewSet,
    GetTokenView,
    RegistrationView,
    ReviewViewSet)

appname = 'api'
router = DefaultRouter()

router.register(r'users', GetAllUserViewSet, basename='users')
router.register(r'genres', GenreViewSet, basename='genres')
router.register(r'titles', TitleViewSet, basename='titles')
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'titles/(?P<title_id>\d+)/reviews',
                ReviewViewSet, basename='reviews')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments')


urlpatterns = [
    path('v1/', include(router.urls)),
    path(
        'v1/auth/signup/',
        RegistrationView.as_view(),
        name='registration'),
    path(
        'v1/auth/token/',
        GetTokenView.as_view(),
        name='get_token'
    )
]

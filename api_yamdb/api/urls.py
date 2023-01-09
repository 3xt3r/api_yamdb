from rest_framework.routers import DefaultRouter
from .views import 
from django.urls import include, path


router = DefaultRouter()
router.register(r'^titles/(?P<title_id>\d+)/review', ReviewViewSet, basename='review')
router.register(r'^titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments', CommentViewSet, basename='comments')
router.register(r'^titles/(?P<title_id>\d+)/rating', RatingViewSet)


urlpatterns = [
    path('v1/', include(router.urls)),
]
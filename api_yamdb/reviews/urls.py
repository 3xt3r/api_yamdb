from django.urls import path

from . import views

app_name = 'reviews'

urlpatterns = [
    path('titles/<int:title_id>/review/',
         views.add_review, name='add_review'),
    path('titles/<int:title_id>/reviews/<int:review_id/comments>',
         views.add_comment, name='add_comment'),
    path('titles/<int:title_id>/rating', views.rating, name='rating'),
]
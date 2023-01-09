from rest_framework import viewsets, permissions

from reviews.models import Review, Comment
from .serializers import ReviewSerializer, CommentSerializer

from django.shortcuts import get_object_or_404
from .permissions import AuthorOrReadOnly
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import filters, mixins


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [AuthorOrReadOnly]
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        return title.reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [AuthorOrReadOnly]
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get("review_id"))
        return review.comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


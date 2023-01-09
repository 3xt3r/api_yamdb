from django.shortcuts import render, get_object_or_404, redirect
from .models import Review, Comment
from .forms import ReviewForm, CommentForm
from django.contrib.auth.decorators import login_required


@login_required
def add_review(request, title_id):
    reviews = Review.objects.filter(title_id=title_id)
    for review_for_title in reviews:
        if review_for_title.author != request.user:
            form = ReviewForm(request.POST or None)
            if form.is_valid():
                review = form.save(commit=False)
                review.author = request.user
                review.title_id = title_id
                review.save()
    return redirect('titles:title_detail', title_id=title_id)


@login_required
def add_comment(request, title_id, review_id):
    comment = get_object_or_404(Comment, pk=review_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.title_id = title_id
        comment.review_id = review_id
        comment.save()
    return redirect('titles:title_detail', title_id=title_id)


def rating(request, title_id):
    title = Title.objects.filter(title_id=title_id)
    title_reviews = title.reviews.all()
    title_rating = 0
    for review in title_reviews:
        title_rating += review.score
    return redirect('titles:title_detail', title_id=title_id)
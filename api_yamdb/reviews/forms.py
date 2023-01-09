from django import forms
from .models import Review, Comment


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('text', 'score', )
        labels = {'text': 'Отзыв', 'score': 'Оценка'}
        help_text = {'text': 'Введите текст отзыва', 'score': 'Выберите оценку'}


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text', )
        labels = {'text': 'Комментарий'}
        help_text = {'text': 'Введите текст комментария'}
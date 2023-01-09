from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User = get_user_model()

CHOICES = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8'),
        ('9', '9'),
        ('10', '10'),
    )

class Review(models.Model):
    text = models.CharField(max_length=500)
    score = models.CharField(max_length=10, choices = CHOICES)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    pub_date = models.DateTimeField(auto_now_add=True)
    title_id = models.ForeignKey(
        Title,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='reviews'
    )

    def __str__(self):
        return self.text


class Comment(models.Model):
    text = models.CharField(max_length=500)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(auto_now_add=True)
    title_id = models.ForeignKey(
        Title,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='comments'
    )
    review_id = models.ForeignKey(
        Review,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='comments'
    )

    def __str__(self):
        return self.text
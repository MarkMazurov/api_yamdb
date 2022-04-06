from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import CustomUser


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=200)
    year = models.PositiveSmallIntegerField()
    description = models.TextField()
    genre = models.ManyToManyField(Genre, related_name='genres')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        null=True
    )

    def __str__(self):
        return self.name


class Review(models.Model):
    reviewed_item = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text = models.TextField()
    item_rating = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    pub_date = models.DateTimeField(
        'Дата публикации отзыва',
        auto_now_add=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=[
                'reviewed_item',
                'item_rating',
                'author'
            ], name='unique_rating')
        ]


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(
        'Дата публикации комментария',
        auto_now_add=True,
    )

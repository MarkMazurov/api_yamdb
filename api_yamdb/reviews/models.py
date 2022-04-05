from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Genre(models.Model):
    pass


class Category(models.Model):
    pass


class Title(models.Model):
    name = models.CharField(max_length=200)
    year = models.PositiveSmallIntegerField()
    # rating = ???
    description = models.TextField()
    genre = models.ForeignKey(
        Genre,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='titles',
        null=True
    )
    category = models.ForeignKey(
        Category,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='titles',
        null=True
    )


class Review(models.Model):
    reviewed_item = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews')
    # author = models.ForeignKey(User, on_delete=models.CASCADE)
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
                # 'author'
            ], name='unique_rating')
        ]


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField()
    # author = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(
        'Дата публикации комментария',
        auto_now_add=True,
    )

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
        on_delete=models.SET_NULL,
        related_name='titles'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles'
    )

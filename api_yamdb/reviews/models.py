from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from users.models import User


class Category(models.Model):
    """Категории произведений."""
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)

    class Meta():
        ordering = ('name',)

    def __str__(self):
        return self.name[:20]


class Genre(models.Model):
    """Жанры произведений; у произведения может быть несколько жанров."""
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)

    class Meta():
        ordering = ('name',)

    def __str__(self):
        return self.name[:20]


class Title(models.Model):
    """Произведения (книги, фильмы, музыка и пр.)."""
    name = models.CharField(max_length=256)
    year = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='titles',
    )
    genre = models.ManyToManyField(Genre, db_table='title_genres')

    class Meta():
        ordering = ('name',)

    def __str__(self):
        return self.name[:30]


class Review(models.Model):
    """Отзывы пользователей и их оценки произведений"""
    text = models.TextField(verbose_name='Отзыв')
    score = models.IntegerField(
        verbose_name='Пользовательская оценка',
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ])
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата отзыва'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    class Meta:
        ordering = ('-created',)

from django.db import models


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
    genres = models.ManyToManyField(Genre, db_table='title_genres')

    class Meta():
        ordering = ('name',)

    def __str__(self):
        return self.name[:30]

from django.db import models

from .validators import validate_year


class Category(models.Model):
    name = models.CharField(
        verbose_name='название категории',
        max_length=200
    )
    slug = models.SlugField(
        verbose_name='слаг категории',
        unique=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        return f'{self.name} {self.name}'


class Genre(models.Model):
    name = models.CharField(
        verbose_name='название жанра',
        max_length=200
    )
    slug = models.SlugField(
        verbose_name='cлаг жанра',
        unique=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ['name']

    def __str__(self):
        return f'{self.name} {self.name}'


class Title(models.Model):
    name = models.CharField(
        verbose_name='название',
        max_length=200,
        db_index=True
    )
    year = models.PositiveSmallIntegerField(
        verbose_name='год',
        validators=(validate_year, )
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='категория',
        null=True,
        blank=True
    )
    description = models.TextField(
        verbose_name='описание',
        max_length=255,
        null=True,
        blank=True
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='жанр'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ['name']

    def __str__(self):
        return self.name

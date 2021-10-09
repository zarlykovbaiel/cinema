from datetime import date

from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=60, verbose_name='Категория')
    url = models.SlugField(max_length=150, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Категории'
        verbose_name = 'Категория'


class Human(models.Model):
    name = models.CharField(verbose_name='Имя', max_length=100)
    age = models.PositiveIntegerField(verbose_name='Возраст', default=0)
    description = models.TextField(verbose_name='О нём')
    image = models.ImageField(upload_to='actor/', verbose_name='Изображение')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Актеры'
        verbose_name = 'Актер'


class Genre(models.Model):
    name = models.CharField(verbose_name='Название', max_length=100)
    description = models.TextField(verbose_name='Описание')
    url = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Жанры'
        verbose_name = 'Жанр'


class Movie(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    tagline = models.CharField(max_length=255, verbose_name='Слоган', default='')
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(verbose_name='Постер', upload_to='movies/')
    year = models.PositiveSmallIntegerField(verbose_name='Дата выпуска', default=2021)
    country = models.CharField(verbose_name='Страна', max_length=100)
    directors = models.ManyToManyField(Human, verbose_name='Режиссёр', related_name='film_director')
    actors = models.ManyToManyField(Human, verbose_name='Актёр', related_name='film_actors')
    genres = models.ManyToManyField(Genre, verbose_name='Жанры')
    world = models.DateField(verbose_name='Примьера в мире', default=date.today)
    budget = models.PositiveIntegerField(verbose_name='Бюджет', default=0, help_text='Укажите сумму в Долларах')
    fees_in_usa = models.PositiveIntegerField(verbose_name='Сборы в США', default=0,
                                              help_text='Укажите сумму в Долларах')
    fees_in_world = models.PositiveIntegerField(verbose_name='Сборы в Мире', default=0,
                                                help_text='Укажите сумму в Долларах')
    category = models.ForeignKey(Category, verbose_name='Категориия', on_delete=models.SET_NULL, null=True)
    # SlugField - слова в url, для маршрутизатора
    url = models.SlugField(max_length=100, unique=True)
    # черновик
    draft = models.BooleanField(verbose_name='Черновик', default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('movie_detail', kwargs={'slug': self.url})

    def get_review(self):
        return self.reviews_set.filter(parent_isnull=True)

    class Meta:
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'

class MovieShots(models.Model):
    title = models.CharField(verbose_name='Название', max_length=150)
    description = models.TextField(verbose_name='Описание')
    images = models.ImageField(verbose_name='Изображение', upload_to='movieshots/')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name='Фильм')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Кадр фильма'
        verbose_name_plural = 'Кадры Фильма'


class RatingStar(models.Model):
    value = models.SmallIntegerField(verbose_name='Значение', default=0)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name='Фильмы')

    def __str__(self):
        return self.value

    class Meta:
        verbose_name = 'Звёзда Рейтинга'
        verbose_name_plural = 'Звёзды Рейтинга'


class Review(models.Model):
    email = models.EmailField(verbose_name='Почта')
    name = models.CharField(max_length=50, verbose_name='Имя')
    text = models.TextField(blank=True, verbose_name='Отзывы')
    # SET_NULL - удаляет только определенное значение
    # null = True - ссылается к базе данных для того чтобы можно было оставлять пустое значение
    parent = models.ForeignKey('self', verbose_name='Родитель', on_delete=models.SET_NULL, blank=True,
                               null=True, related_name='children', )
    movie = models.ForeignKey(Movie, verbose_name='Фильм', on_delete=models.CASCADE, related_name='reviews')

    def __str__(self):
        return f'{self.name}={self.movie}'

    class Meta:
        verbose_name_plural = 'Отзывы'
        verbose_name = 'Отзыв'


from django.db import models


class User(models.Model):
    email = models.EmailField(verbose_name='Электронная почта', unique=True) #Уникальный email пользователя
    last_name = models.CharField(verbose_name='Фамилия', max_length=256) #Фамилия пользователя
    first_name = models.CharField(verbose_name='Имя', max_length=256) #Имя пользователя
    middle_name = models.CharField(verbose_name='Отчество', max_length=256) #Отчество пользователя
    phone = models.CharField(verbose_name='Номер телефона', max_length=11) #Номер телефона пользователя

    def __str__(self):
        return f'{self.pk} {self.last_name} {self.first_name} {self.middle_name}'


class Coords(models.Model):
    latitude = models.FloatField(verbose_name='Широта') #Широта
    longitude = models.FloatField(verbose_name='Долгота') #Долгота
    height = models.IntegerField(verbose_name='Высота над уровнем моря') #Высота над уровнем моря в метрах

    def __str__(self):
        return f'latitude:{self.latitude} longitude:{self.longitude} height:{self.height}'


class Pereval(models.Model):
    NEW, PENDING, ACCEPTED, REJECTED = 'NE', 'PE', 'AC', 'RE' 
    STATUS_CHOICES = [
        (NEW, 'new'),
        (PENDING, 'pending'),
        (ACCEPTED, 'accepted'),
        (REJECTED, 'rejected')
    ]
    status = models.CharField(verbose_name='Статус', max_length=2, choices=STATUS_CHOICES, default=NEW) #Статус модерации
    user = models.ForeignKey(User, on_delete=models.CASCADE) #Связь с пользователем, добавившим информацию
    coords = models.OneToOneField(Coords, on_delete=models.CASCADE) #Координаты перевала
    beauty_title = models.CharField(verbose_name='Тип местности', max_length=256) #Тип местности
    title = models.CharField(verbose_name='Название', max_length=256) #Название перевала
    other_titles = models.CharField(verbose_name='Другие названия', max_length=256) #Альтернативные названия
    connect = models.TextField(verbose_name='Сопроводительный текст', blank=True) #Дополнительная информация
    datetime = models.DateTimeField(auto_now_add=True) #
    level_spring = models.CharField(verbose_name='Уровень сложности весной', max_length=5, blank=True) #Уровень сложности
    level_summer = models.CharField(verbose_name='Уровень сложности летом', max_length=5, blank=True) #Уровень сложности
    level_autumn = models.CharField(verbose_name='Уровень сложности осенью', max_length=5, blank=True) #Уровень сложности
    level_winter = models.CharField(verbose_name='Уровень сложности зимой', max_length=5, blank=True) #Уровень сложности
 



class Image(models.Model):
    pereval = models.ForeignKey(Pereval, on_delete=models.CASCADE, related_name='images') #Связь с перевалом
    data = models.URLField() #URL изображения
    title = models.CharField(verbose_name='Примечание', max_length=256, blank=True) #Описание изображения
    datetime = models.DateField(auto_now_add=True) #Дата добавления изображения

    def __str__(self):
        return f'{self.title} - {self.pereval}'

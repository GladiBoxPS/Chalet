from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission


class User(AbstractUser):
    photo = models.ImageField(upload_to="", blank=True, verbose_name="Фотография")
    date_birth = models.DateTimeField(blank=True, null=True, verbose_name="Дата рождения")
    phone = models.PositiveIntegerField(null=True, verbose_name="Номер телефона")
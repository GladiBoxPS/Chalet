# Generated by Django 4.2.7 on 2023-11-16 08:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('main', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='phone',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservation_phone', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='reservation',
            name='table',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.table'),
        ),
        migrations.AddField(
            model_name='reservation',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservation_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='menu',
            name='cat',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='posts', to='main.category', verbose_name='Категории'),
        ),
        migrations.AddField(
            model_name='menu',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='tags', to='main.tagpost', verbose_name='Теги'),
        ),
    ]

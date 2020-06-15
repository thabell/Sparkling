# Generated by Django 3.0.7 on 2020-06-13 15:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0018_auto_20200613_2058'),
    ]

    operations = [
        migrations.CreateModel(
            name='Letter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Текст отзыва, жалобы, пожелания')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Дата')),
                ('viewed', models.BooleanField(default=False, verbose_name='Просмотрено')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='letter', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Письмо',
                'verbose_name_plural': 'Письма',
                'ordering': ['viewed', '-date'],
            },
        ),
    ]
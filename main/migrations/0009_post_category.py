# Generated by Django 3.0.7 on 2020-06-13 05:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_auto_20200613_1148'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='category',
            field=models.CharField(choices=[('Спорт', 'Спорт'), ('Технологии', 'Технологии'), ('Путешествия', 'Путешествия'), ('Разное', 'Разное')], default=1, max_length=30, verbose_name='Категория'),
            preserve_default=False,
        ),
    ]
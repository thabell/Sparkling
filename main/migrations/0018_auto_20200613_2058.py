# Generated by Django 3.0.7 on 2020-06-13 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0017_auto_20200613_1702'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.ManyToManyField(blank=True, default=[4], related_name='post', to='main.Category'),
        ),
    ]

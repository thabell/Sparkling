# Generated by Django 3.0.7 on 2020-06-12 14:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_tag_colr'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Tag',
            new_name='Category',
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Категория', 'verbose_name_plural': 'Категории'},
        ),
        migrations.RenameField(
            model_name='post',
            old_name='tag',
            new_name='category',
        ),
    ]
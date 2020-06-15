# Generated by Django 3.0.7 on 2020-06-13 10:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_auto_20200613_1537'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='part',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='category', to='main.Part'),
        ),
        migrations.AlterField(
            model_name='post',
            name='tag',
            field=models.ManyToManyField(blank=True, related_name='post', to='main.Tag'),
        ),
    ]
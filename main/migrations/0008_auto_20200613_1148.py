# Generated by Django 3.0.7 on 2020-06-13 04:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_post_tag'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='postparagraph',
            name='post',
        ),
        migrations.RemoveField(
            model_name='post',
            name='category',
        ),
        migrations.AddField(
            model_name='post',
            name='content',
            field=models.TextField(blank=True, default='_', help_text='Вы можете писать в виде html-разметки или просто текст', verbose_name='Текст статьи'),
        ),
        migrations.AlterField(
            model_name='post',
            name='annotation',
            field=models.CharField(max_length=200, verbose_name='Краткая аннотация'),
        ),
        migrations.AlterField(
            model_name='post',
            name='number',
            field=models.IntegerField(blank=True, default=9999, help_text='Необязательное поле. Ненумерованные статьи располагаются после нумерованых в порядке их создания', null=True, verbose_name='№ в последовательности статей'),
        ),
        migrations.AlterField(
            model_name='post',
            name='preview',
            field=models.ImageField(blank=True, default='main/post/preview/def_post_img.jpg', upload_to='main/post/preview', verbose_name='Изображение'),
        ),
        migrations.AlterField(
            model_name='userdata',
            name='photo',
            field=models.ImageField(blank=True, default='main/user_data/photo/def_ava.jpg', upload_to='main/user_data/photo', verbose_name='Фото (квадратное)'),
        ),
        migrations.DeleteModel(
            name='Element',
        ),
        migrations.DeleteModel(
            name='PostParagraph',
        ),
    ]

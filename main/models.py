from django.db import models

# Create your models here.

from django.contrib.auth.models import User


class UserData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_data")
    photo = models.ImageField('Фото', upload_to='main/user_data/photo', blank=True, default="main/user_data/photo/def_ava.jpg", help_text="Портретная ориентация, лучше квадратное изображение")
    annotation = models.CharField("Кратко о Вас", max_length=200, default=" ")

    def __str__(self):
        return "Данные пользователя " + str(self.user) + ": " + str(self.photo)


class Part(models.Model):
    name = models.CharField("Название", max_length=20)

    class Meta:
        verbose_name = "Раздел"
        verbose_name_plural = "Разделы"

    def __str__(self):
        return str(self.name)


class Category(models.Model):
    name = models.CharField("Название", max_length=20)
    colr = models.CharField("Цвет", max_length=10)
    part = models.ForeignKey(Part, on_delete=models.SET_DEFAULT, related_name="category", default=Part.objects.get(name="Вдохновение").id)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return str(self.name)

class Tag(models.Model):
    name = models.CharField("Название", max_length=20)

    class Meta:
        verbose_name = "Тэг"
        verbose_name_plural = "Тэги"

    def __str__(self):
        return str(self.name)

    @classmethod
    def create(cls, name):
        tagg = cls(name=name)
        return tagg

class Post(models.Model):
    number = models.CharField("№ в последовательности статей", max_length=4,
                              null=True, blank=True, default="~",
                              help_text="*Необязательное поле. Ненумерованные статьи располагаются после нумерованых в порядке их создания")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post")
    title = models.CharField("Название", max_length=100)
    annotation = models.CharField("Краткая аннотация", max_length=200)
    preview = models.ImageField('Изображение', upload_to='main/post/preview',
                                blank=True, default="main/post/preview/def_post_img.jpg")
    # category = models.CharField("Категория", max_length=30, default="Разное",
    #                             choices=list(map(lambda x: (x.name, x.name), Category.objects.all())))
    category = models.ManyToManyField(Category, related_name="post", blank=True,
                                      default=[Category.objects.get(name="Разное").id],
                                      help_text="*Удерживайте «Control» или «Command» на Mac, чтобы выбрать более одного")
    tag = models.ManyToManyField(Tag, related_name="post", blank=True,
                                 help_text="*Удерживайте «Control» или «Command» на Mac, чтобы выбрать более одного")
    date = models.DateTimeField("Дата", auto_now_add=True)
    content = models.TextField("Текст статьи", blank=True, default="",
                               help_text="*Вы можете писать в виде html-разметки или просто текст<br>**Потяните за угол, чтоб изменить размер этого поля")
    moderated = models.BooleanField("Прошла проверку", default=False)

    # def get_category_color(self):
    #     return Category.objects.get(name=self.category).colr or " "

    def categories_to_str(self):
        return ", ".join(map(str, self.category.all()))

    def tags_to_str(self):
        return ", ".join(map(str, self.tag.all()))

    class Meta:
        ordering = ['number', 'id']
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"

    def __str__(self):
        return str(self.user) + " - " + str(self.title)

    def get_html(self):
        return str(self.content)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment", null=True)
    date = models.DateTimeField("Дата", auto_now_add=True)
    text = models.TextField("Текст")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comment")

    def __str__(self):
        return str(self.user) + ". Коммент. на статью № " + str(self.post.number)\
               + ", " + str(self.date.strftime('%Y-%m-%d %H:%M')) + ": " + str(self.text)


class Letter(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="letter", null=True)
    text = models.TextField('Текст отзыва, жалобы, пожелания')
    date = models.DateTimeField("Дата", auto_now_add=True)
    viewed = models.BooleanField("Просмотрено", default=False)

    class Meta:
        ordering = ['viewed', '-date']
        verbose_name = "Письмо"
        verbose_name_plural = "Письма"

    def __str__(self):
        return "Отзыв № " + str(self.id) + " от " + self.date.strftime('%Y-%m-%d %H:%M')

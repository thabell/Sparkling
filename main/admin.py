from django.contrib import admin
from main import models as my_models
from django.contrib.auth.models import User

class UserDataInline(admin.TabularInline):
    model = my_models.UserData

class PostInline(admin.TabularInline):
    model = my_models.Post

class CommentInline(admin.TabularInline):
    model = my_models.Comment

admin.site.unregister(User)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    inlines = [UserDataInline, PostInline, CommentInline, ]


admin.site.register(my_models.Category)


class CategoryInline(admin.TabularInline):
    model = my_models.Category

@admin.register(my_models.Part)
class PartAdmin(admin.ModelAdmin):
    inlines = [CategoryInline, ]


admin.site.register(my_models.Tag)


@admin.register(my_models.Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'moderated', 'number', 'id', 'annotation', 'preview', 'categories_to_str', 'tags_to_str', 'date', )
    inlines = [CommentInline, ]


@admin.register(my_models.Letter)
class LetterAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'viewed', 'user', 'text', )

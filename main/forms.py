from django.contrib.auth.models import User
from main.models import UserData, Comment, Letter, Post
from django import forms

class UserForm(forms.ModelForm):
    password = forms.CharField(label="Пароль:", widget=forms.PasswordInput, required=True)
    password_double = forms.CharField(label="Повторно пароль:", widget=forms.PasswordInput, required=True)
    email = forms.CharField(label="E-mail", widget=forms.EmailInput, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password_double', 'email', 'first_name', 'last_name')

    def clean(self):
        cleaned_data = super().clean()
        passw = cleaned_data['password']
        passw_doub = cleaned_data['password_double']
        if passw != passw_doub:
            raise forms.ValidationError("Пароли не совпадают")
        return cleaned_data

class UserDataForm(forms.ModelForm):
    class Meta:
        model = UserData
        fields = ('photo', 'annotation', )


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("text", )


class LetterForm(forms.ModelForm):
    class Meta:
        model = Letter
        fields = ("text", )

class PostForm(forms.ModelForm):
    my_tags = forms.CharField(max_length=50, label="Свои тэги",
                              help_text="*Вы можете добавить свои ключевые слова, введя их через запятую", required=False)

    class Meta:
        model = Post
        fields = ("number", "title", "annotation", "preview", "category", "tag", "my_tags", "content", )

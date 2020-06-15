from . import views as main_views
from django.urls import path
from django.contrib.auth import views as auth_views
from main import models as my_models

urlpatterns = [
    path('', main_views.index, name='index'),
    path('index/', main_views.index, name='index'),
    path('about/', main_views.about, name='about'),
    path('feed/', main_views.feed, name='feed'),
    path('contact/', main_views.contact, name='contact'),
    path('profile/', main_views.profile, name='profile'),
    path('post/', main_views.post, name='post'),
    path('new_post/', main_views.new_post, name='new_post'),
    path('login/', auth_views.LoginView.as_view(extra_context={'parts': my_models.Part.objects.all()}), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', main_views.signup, name='signup'),
]

from django.shortcuts import render, redirect
from main import models as my_models
from random import randint

def index(request):
    three_new_posts = sorted(list(my_models.Post.objects.all()), key=lambda x: x.date, reverse=True)[0:3]
    four_random_posts = []
    i = 0
    while len(four_random_posts) < 4 and i < 1000:
        random_post = my_models.Post.objects.all()[randint(0, my_models.Post.objects.count() - 1)]
        if random_post not in four_random_posts:
            four_random_posts.append(random_post)
        i += 1
    three_random_categ = []
    j = 0
    while len(three_random_categ) < 3 and j < 1000:
        random_cat = my_models.Category.objects.all()[randint(0, my_models.Category.objects.count() - 1)]
        if random_cat not in three_random_categ:
            three_random_categ.append(random_cat)
        j += 1
    return render(request, 'main/index.html', {
        'parts': my_models.Part.objects.all(),
        "four_popular_posts": sorted(list(my_models.Post.objects.all()), key=lambda x: x.comment.count(), reverse=True)[0:4],
        "three_new_posts": three_new_posts,
        "four_random_posts": four_random_posts,
        "three_random_categ": three_random_categ,
    })


def about(request):
    return render(request, 'main/about.html', {
        'parts': my_models.Part.objects.all(),
    })


from django.http import HttpResponseRedirect
from django.urls import reverse
from main.forms import LetterForm
def contact(request):
    if request.method == 'POST':
        letter_form = LetterForm(request.POST)
        new_letter = letter_form.save(commit=False)
        if request.user.is_authenticated:
            new_letter.user = request.user
        new_letter.save()
        return HttpResponseRedirect('{}?sent=True'.format(reverse('contact', kwargs={})))
    else:
        letter_form = LetterForm()
        return render(request, 'main/contact.html', {
            'parts': my_models.Part.objects.all(),
            "letter_form": letter_form,
            "sent": request.GET.get("sent", False),
        })


from django.shortcuts import get_object_or_404
def feed(request):
    if request.method == "POST":
        if "author_search" in request.POST:
            curr_author = get_object_or_404(User.objects, username=request.POST.get("author_search"))
            return HttpResponseRedirect(('{}?author_id=' + str(curr_author.id)).format(reverse('feed', kwargs={})))
    else:
        tags = my_models.Tag.objects.all()
        auth_count = User.objects.count()
        ix = randint(0, auth_count - 1)
        random_user = User.objects.all()[ix:ix + 1][0]
        content = my_models.Post.objects.all()
        curr_author = None
        if "author_id" in request.GET:
            curr_author = get_object_or_404(User.objects, id=request.GET.get("author_id"))
            content = content.filter(user=curr_author)
        curr_category = None
        if "category_id" in request.GET:
            curr_category = get_object_or_404(my_models.Category.objects, id=request.GET.get("category_id"))
            content = content.filter(category=curr_category)
        curr_tag = None
        if "tag_id" in request.GET:
            curr_tag = get_object_or_404(my_models.Tag.objects, id=request.GET.get("tag_id"))
            content = content.filter(tag=curr_tag)
        curr_part = None
        if "part_id" in request.GET:
            curr_part = get_object_or_404(my_models.Part.objects,   id=request.GET.get("part_id"))
            content = content.filter(category__part=curr_part)
        content_len = content.count()
        if "sort" in request.GET:
            sorting = request.GET.get("sort")
            if sorting == "new":
                content = sorted(content, key=lambda x: x.date, reverse=True)
                content_len = len(content)
            elif sorting == "popular":
                content = sorted(content, key=lambda x: x.comment.count(), reverse=True)
                content_len = len(content)
        return render(request, 'main/feed.html', {
            'parts': my_models.Part.objects.all(),
            "tags": tags,
            "random_user": random_user,
            "four_popular_posts": sorted(my_models.Post.objects.all(), key=lambda x: x.comment.count(), reverse=True)[0:4],
            "author_id": request.GET.get("author_id", False),
            "category_id": request.GET.get("category_id", False),
            "tag_id": request.GET.get("tag_id", False),
            "part_id": request.GET.get("part_id", False),
            "sort": request.GET.get("sort", False),
            "curr_author": curr_author,
            "curr_category": curr_category,
            "curr_tag": curr_tag,
            "curr_part": curr_part,
            "content": content,
            "content_len": content_len,
        })


from main.forms import CommentForm
def post(request):
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        new_comment = comment_form.save(commit=False)
        new_comment.user = request.user
        new_comment.post = my_models.Post.objects.get(id=request.GET.get("post_id"))
        new_comment.save()
        return redirect(request.get_full_path())
    else:
        article = get_object_or_404(my_models.Post, id=request.GET.get("post_id"))
        tags = my_models.Tag.objects.all()
        auth_count = User.objects.count()
        ix = randint(0, auth_count - 1)
        random_user = User.objects.all()[ix:ix + 1][0]
        comment_form = CommentForm()
        return render(request, 'main/post.html', {
            "article": article,
            'parts': my_models.Part.objects.all(),
            "tags": tags,
            "random_user": random_user,
            "comment_form": comment_form,
            "four_popular_posts": sorted(list(my_models.Post.objects.all()), key=lambda x: x.comment.count(), reverse=True)[0:4],
        })


from django.contrib.auth.decorators import login_required
from main.forms import PostForm
@login_required(login_url="login")
def new_post(request):
    if request.method == 'POST':
        post_form = PostForm(request.POST, request.FILES)
        new_postt = post_form.save(commit=False)
        new_postt.user = request.user
        new_postt.save()
        categories = request.POST.getlist("category")
        for cat in categories:
            new_postt.category.add(cat)
        tagss = request.POST.getlist("tag")
        for ta in tagss:
            new_postt.category.add(ta)
        my_tags = request.POST.get("my_tags")
        my_tags = my_tags.strip()
        my_tags = my_tags.split(",")
        for ta_g in my_tags:
            n_t = my_models.Tag.objects.create(name=ta_g)
            n_t.save()
            new_postt.tag.add(n_t)
        return HttpResponseRedirect(('{}?post_id=' + str(new_postt.id)).format(reverse('post', kwargs={})))
    else:
        post_form = PostForm()
        return render(request, 'main/new_post.html', {
            'parts': my_models.Part.objects.all(),
            "post_form": post_form,
        })


@login_required(login_url="login")
def profile(request):
    if request.method == "POST":
        if "delete_post" in request.POST:
            print("delete_post")
            request.user.post.get(id=request.POST.get("delete_post")).delete()
            return HttpResponseRedirect('{}'.format(reverse('profile', kwargs={})))
    else:
        return render(request, 'main/profile.html', {
            'parts': my_models.Part.objects.all(),
        })


from main.forms import UserDataForm, UserForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

def signup(request):
    if request.method == "POST":
        user_form = UserForm(request.POST)
        user_data_form = UserDataForm(request.POST)
        if user_form.is_valid() and user_data_form.is_valid():
            new_user = User.objects.create_user(
                user_form.cleaned_data['username'],
                user_form.cleaned_data['email'],
                user_form.cleaned_data['password'])
            new_user.first_name = user_form.cleaned_data['first_name']
            new_user.last_name = user_form.cleaned_data['last_name']
            new_user.save()
            new_user_data = user_data_form.save(commit=False)
            new_user_data.user = new_user
            new_user_data.save()
            user = authenticate(
                username=user_form.cleaned_data['username'],
                password=user_form.cleaned_data['password']
            )
            if user is not None:
                login(request, user)
            else:
                print('invalid login')
            return redirect('index')
    else:
        user_form = UserForm()
        user_data_form = UserDataForm()
        return render(request, 'registration/signup.html', {
            "user_form": user_form,
            "user_data_form": user_data_form,
            'parts': my_models.Part.objects.all(),
        })

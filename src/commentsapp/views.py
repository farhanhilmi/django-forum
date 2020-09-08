from django.shortcuts import render, redirect

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from django.contrib.auth.decorators import login_required

from .models import *
from .forms import *

# Create your views here.

def regiterPage(request):
    form = CreateUser()

    if request.method == 'POST':
        form = CreateUser(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            messages.success(request, 'Account was created for ' + username)
            return redirect('login')

    context = {'form': form}
    return render(request, 'auth/register.html', context)

def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or password is incorrect')

    context = {}
    return render(request, 'auth/login.html', context)

def logoutPage(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def home(request):
    users = request.user.profile.id
    forums = forum.objects.all()
    count = forums.count()
    discussions = []
    # print(request.user.profile.id)
    print(forums)

    for i in forums:
        discussions.append(i.discussion_set.all())

    context = {'forums': forums, 'count': count, 'discussions': discussions}
    return render(request, 'home.html', context)

def viewForum(request,pk):
    forum_id = forum.objects.get(id=pk)
    discuss_id = Discussion.objects.filter(forum_id=forum_id.id)
    profiles = profile.objects.all()
    # print(discuss_id.discuss)
    # discuss = discuss_id.filter(forum=forum_id.topic)

    context = {'forum': forum_id, 'discuss': discuss_id}
    return render(request, 'view_forum.html', context)

def addInForum(request):
    # profiles = request.user.profile
    form = CreateInForum()
    # print(forum)
    # print(profiles)
    if request.method == 'POST':
        form = CreateInForum(request.POST)
        if form.is_valid():
            data = form.save()
            data.profile = profile.objects.get(id=request.user.profile.id)
            data.save()
            return redirect('/')

    context = {'form': form}
    return render(request, 'addInForum.html', context)

def addInDiscussion(request,pk):
    form = CreateInDiscussion()
    if request.method == 'POST':
        form = CreateInDiscussion(request.POST)
        if form.is_valid():
            data = form.save()
            data.forum = forum.objects.get(id=pk)
            data.user = User.objects.get(id=request.user.id)
            data.save()
            return redirect('/')
    
    context = {'form': form}
    return render(request, 'addInDiscussion.html', context)
from django.shortcuts import render, redirect

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum

from django.http import HttpResponseRedirect

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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
    forums = forum.objects.all().annotate(total=Sum('profile')).order_by('-date_created')
    popular = forum.objects.all().order_by('num_comment')

    page = request.GET.get('page', 1)
    paginator = Paginator(forums, 10)

    countForum = forums.count()
    discussions = []

    for i in forums:
        discussions.append(i.discussion_set.all())

    try:
        forums = paginator.page(page)
    except PageNotAnInteger:
        forums = paginator.page(1)
    except EmptyPage:
        forums = paginator.page(paginator.num_pages)
    
    print(forums)


    context = {'forums': forums, 'countForum': countForum, 'discussions': discussions, 'popular':popular}
    return render(request, 'home.html', context)

def viewForum(request,pk):
    forum_id = forum.objects.annotate(total=Sum('profile')).get(id=pk)
    discuss_id = Discussion.objects.filter(forum_id=forum_id.id)
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
            data.num_comment = 0
            data.save()
            return redirect('/')

    context = {'form': form}
    return render(request, 'addInForum.html', context)

def deleteForum(request,pk):
    forums = forum.objects.get(id=pk)
  
    forums.delete()
    return redirect('/')


def likeComment(request,pk):
    discuss = Discussion.objects.get(id=pk)
    discuss.like = discuss.like + 1
    discuss.save()

    return redirect('/')


def addInDiscussion(request,pk):
    forums = forum.objects.get(id=pk)
    comment = updateCommentForm(instance=forums)
    
    print(type(forums.num_comment))
    print(forums.num_comment)

    form = CreateInDiscussion()
    if request.method == 'POST':
        comment = updateCommentForm(request.POST, instance=forums)
        form = CreateInDiscussion(request.POST)
        if form.is_valid() and comment.is_valid():
            dataComment = comment.save()
            data = form.save()
            dataComment.num_comment = forums.num_comment + 1
            data.forum = forum.objects.get(id=pk)
            data.user = User.objects.get(id=request.user.id)
            data.like = 0

            dataComment.save()
            data.save()

            return redirect('/')
    
    context = {'form': form,'comment': comment}
    return render(request, 'addInDiscussion.html', context)
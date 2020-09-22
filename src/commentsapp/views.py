from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from django.http import HttpResponseRedirect

from django.db.models import Count, Sum

from django.http import HttpResponseRedirect

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import *
from .forms import *

# Create your views here.

def registerPage(request):
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

@login_required(login_url='login')
def logoutPage(request):
    logout(request)
    return redirect('login')

# @login_required(login_url='login')
def home(request):
    forums = forum.objects.all().annotate(total=Sum('profile')).order_by('-date_created')
    popular = forum.objects.all().order_by('num_comment')
    category = Category.objects.all().order_by('category')

    title = "Lates Forum"

    page = request.GET.get('page', 1)
    paginator = Paginator(forums, 10)

    countForum = forums.count()
    discussions = []

    print(request.user.id)

    for i in forums:
        discussions.append(i.discussion_set.all())

    try:
        forums = paginator.page(page)
    except PageNotAnInteger:
        forums = paginator.page(1)
    except EmptyPage:
        forums = paginator.page(paginator.num_pages)
    

    context = {'forums': forums, 'countForum': countForum, 
    'discussions': discussions, 'popular':popular, 'category':category, 'title':title}
    return render(request, 'home.html', context)

def myProfilePage(request, username):
    user = User.objects.get(username=username)
    data = profile.objects.get(user_id=user.id)
    forums = forum.objects.all().filter(profile_id=data.id)

    print(request.user.profile.profile_pic)
    context = {'data':data, 'forums':forums}
    return render(request, 'profile.html', context)

def categoryPage(request,pk):
    popular = forum.objects.all().order_by('num_comment')
    category = Category.objects.all().order_by('category')
    # filter_category = category.filter(category__contains=name)
    filter_category = forum.objects.filter(category_id=pk)

    # cat = category.filter(id=pk).cat.first()
    # print(cat.first())
    title = str(category.filter(id=pk).first()) +  " category"

    page = request.GET.get('page', 1)
    paginator = Paginator(filter_category, 10)

    try:
        filter_category = paginator.page(page)
    except PageNotAnInteger:
        filter_category = paginator.page(1)
    except EmptyPage:
        filter_category = paginator.page(paginator.num_pages)

    

    context = {'forums':filter_category, 'category':category, 'popular':popular, 'title':title}
    return render(request, 'home.html', context)

def searchPage(request):
    popular = forum.objects.all().order_by('num_comment')
    category = Category.objects.all().order_by('category')
    name = request.GET.get("searchVal")
    forums = forum.objects.all().filter(topic__contains=name)
    # forums = forum.objects.filter(category_id=pk)

    title = "Search Result"

    page = request.GET.get('page', 1)
    paginator = Paginator(forums, 10)

    try:
        forums = paginator.page(page)
    except PageNotAnInteger:
        forums = paginator.page(1)
    except EmptyPage:
        forums = paginator.page(paginator.num_pages)

    print(forums)

    context = {'forums':forums, 'category':category, 'popular':popular, 'title':title}
    return render(request, 'home.html', context)

def viewForum(request,pk):
    forum_id = forum.objects.annotate(total=Sum('profile')).get(id=pk)
    discuss_id = Discussion.objects.filter(forum_id=forum_id.id).order_by('-date_created')

    popular = forum.objects.all().order_by('num_comment')
    category = Category.objects.all().order_by('category')

    page = request.GET.get('page', 1)
    paginator = Paginator(discuss_id, 10)

    try:
        discuss_id = paginator.page(page)
    except PageNotAnInteger:
        discuss_id = paginator.page(1)
    except EmptyPage:
        discuss_id = paginator.page(paginator.num_pages)


    comment = updateCommentForm(instance=forum_id)
    form = CreateInDiscussion()
    if request.method == 'POST':
        comment = updateCommentForm(request.POST, instance=forum_id)
        form = CreateInDiscussion(request.POST)
        if form.is_valid() and comment.is_valid():
            dataComment = comment.save()
            data = form.save()
            dataComment.num_comment = forum_id.num_comment + 1
            data.forum = forum.objects.get(id=pk)
            data.user = User.objects.get(id=request.user.id)
            data.like = 0

            dataComment.save()
            data.save()

            # return redirect('/view_forum')
            return HttpResponseRedirect(request.path_info)
    

    
    # print(discuss_id.discuss)
    # discuss = discuss_id.filter(forum=forum_id.topic)

    context = {'forum': forum_id, 'discuss': discuss_id, 'popular':popular, 
    'category':category, 'form': form,'comment': comment}
    return render(request, 'view_forum.html', context)

@login_required(login_url='login')
def addInForum(request):
    # profiles = request.user.profile
    form = CreateInForum()
    popular = forum.objects.all().order_by('num_comment')
    category = Category.objects.all().order_by('category')

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

    context = {'form': form, 'category':category, 'popular':popular}
    return render(request, 'addInForum.html', context)

@login_required(login_url='login')
def deleteForum(request,pk):
    forums = forum.objects.get(id=pk)

    if forums.profile.user.id == request.user.id:
        forums.delete()

    return redirect('/')

@login_required(login_url='login')
def likeComment(request,pk):
    discuss = Discussion.objects.get(id=pk)
    discuss.like = discuss.like + 1
    discuss.save()

    return redirect('/')

@login_required(login_url='login')
def addInDiscussion(request,pk):
    forums = forum.objects.get(id=pk)
    comment = updateCommentForm(instance=forums)

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
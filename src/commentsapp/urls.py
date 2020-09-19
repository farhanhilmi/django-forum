from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('login/', views.loginPage, name='login'),
    path('register/', views.registerPage, name='register'),
    path('logout/', views.logoutPage, name='logout'),

    path('profile/<str:username>', views.myProfilePage, name='myProfile'),

    path('category/<str:pk>', views.categoryPage, name='category'),
    path('search/?$', views.searchPage, name='search'),

    path('view_forum/<str:pk>', views.viewForum, name='view_forum'),
    path('addInForum/', views.addInForum, name='addInForum'),
    path('deleteForum/<str:pk>', views.deleteForum, name='deleteForum'),

    path('addInDiscussion/<str:pk>/', views.addInDiscussion, name='addInDiscussion'),
    path('likeComment/<str:pk>/', views.likeComment, name='likeComment'),

]
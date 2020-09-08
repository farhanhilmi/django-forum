from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('login/', views.loginPage, name='login'),
    path('register/', views.regiterPage, name='register'),
    path('logout/', views.logoutPage, name='logout'),

    path('view_forum/<str:pk>', views.viewForum, name='view_forum'),
    path('addInForum/', views.addInForum, name='addInForum'),
    path('addInDiscussion/<str:pk>/', views.addInDiscussion, name='addInDiscussion'),

]
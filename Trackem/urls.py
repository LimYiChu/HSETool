"""Trackem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from userT import views as userView
from UploadExcel import views as UploadV
from userT import views as UserView
from django.contrib.auth import views as auth_views
urlpatterns = [
      # Load excel actions, routes ,
        path('upload/', UploadV.Load, name='Load' ),
        path('LoadRoutes/', UploadV.LoadRoutes, name='LoadRoutes' ),
        path('login/',auth_views.LoginView.as_view(template_name='userT/login.html'),name='login'),
        path('logout/',auth_views.LogoutView.as_view(template_name='userT/logout.html'),name='logout'),
        path('register/', userView.register, name='register' ),
        path('admin/', admin.site.urls, name='adminT'),
       # path('routes/', UserView.yourRoutes.as_view(), name='yourRoutes' ),
        path('main/', UserView.mainDashboard, name='main' ),
       
        path('ActioneeList/', UserView.ActioneeList.as_view(), name='UserActionList' ),
        #path('UA/', UserView.yourActions.as_view(), name='UserActions' ),
        re_path(r'^(?P<id>\d+)/$', userView.getActionDetails,name='getActionsDetails'),
        path('password_reset/', auth_views.PasswordResetView.as_view(template_name='userT/reset.html') ,name='password_reset'),
        path('routesX/', userView.getuserRoutes, name='routesX' ),
        #path('ActioneeList/<int:pk>/', userView.ActionDetails(),name='ActionsDetails'),
        path('ActionDetails/', UserView.ActionDetailsForm.as_view(), name='DetailsForm' ),
        #path('count/', userView.mainDashCount, name='count' ),
        #path('UA/', UserView.UserActions, name='UserActions' ),
      ]

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
#testing for redirect url when not logged in
from django.contrib.auth.decorators import login_required
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
      # Load excel actions, routes ,
        path('upload/', login_required(UploadV.Load), name='Load' ),
        path('LoadRoutes/', login_required(UploadV.LoadRoutes), name='LoadRoutes' ),
        path('login/',auth_views.LoginView.as_view(template_name='userT/login.html'),name='login'),
        path('logout/',auth_views.LogoutView.as_view(template_name='userT/logout.html'),name='logout'),
        path('register/', userView.register, name='register' ),
        path('admin/', admin.site.urls, name='adminT'),
       # path('routes/', UserView.yourRoutes.as_view(), name='yourRoutes' ),
        #to prevent authorised view, add login_required() in front of the views, for example--> login_required(userView.mainDashboard)
        path('main/', login_required(UserView.mainDashboard), name='main' ),
        path('accounts/login/', auth_views.LoginView.as_view(template_name='userT/login.html'),name='login'),
        path('ActioneeList/', login_required(UserView.ActioneeList.as_view()), name='UserActionList' ),
                #path('UA/', UserView.yourActions.as_view(), name='UserActions' ),
        re_path(r'^(?P<id>\d+)/$', userView.getActionDetails,name='getActionsDetails'),
       # path('password_reset/', auth_views.PasswordResetView.as_view(template_name='userT/reset.html') ,name='password_reset'),
        path('routesX/', userView.getuserRoutes, name='routesX' ),
        path('main/', UserView.mainDashboard, name='main' ),
       
       #List path using class listview to get actionee and approver
        path('ActioneeList/', UserView.ActioneeList.as_view(), name='UserActionList' ),
        path('ApproverList/', UserView.ApproverList.as_view(), name='ApproverList' ),

       
        re_path(r'^(?P<id>\d+)/$', userView.getActionDetails,name='getActionsDetails'),
       
        path('routesX/', userView.getuserRoutes, name='routesX' ),
        #path('ActioneeList/<int:pk>/', userView.ActionDetails(),name='ActionsDetails'),
       
        
        #path('count/', userView.mainDashCount, name='count' ),
        #path('UA/', UserView.UserActions, name='UserActions' ),

        #Following urls are for actionee approvers updates and approvals
        path('ActioneeList/<int:pk>/update', UserView.ActioneeItemsMixin.as_view(), name='ActioneeFormMixin' ),
        path('ActioneeList/<int:id>/', UserView.DetailActioneeItems.as_view(), name='DetailsForm' ),
        #path('ApproverList/<int:id>/approve', UserView.ApproveItems.as_view(), name='ApproveForm' ),
        path('ApproverList/<int:pk>/approve', UserView.ApproveItemsMixin.as_view(), name='ApproveFormMixin' ),

        #Following URLs are for reseting and changing password. Note that the reset password via email is yet to be set up. Right now please obtain the link in the terminal upon requesting password reset.
        path('password_change/done/',auth_views.PasswordChangeDoneView.as_view(template_name='userT/password_change_done.html'),name='password_change_done'),
        path('password_change/',auth_views.PasswordChangeView.as_view(template_name='userT/password_change.html'),name='password_change'),
        path('password_reset/done/',auth_views.PasswordResetCompleteView.as_view(template_name='userT/password_reset_done.html'),name='password_reset_done'),
        path('reset/<uidb64>/<token>',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
        path('password_reset/',auth_views.PasswordResetView.as_view(template_name='userT/password_reset_form.html'),name='password_reset'),
        path('reset/done/',auth_views.PasswordResetCompleteView.as_view(template_name='userT/password_reset_complete.html'),name='password_reset_complete'),
        path('ContactUs/',UserView.ContactUs,name='ContactUs'),
        
        
        #path('ContactUs/',UserView.ContactUs,name='ContactUs'),

        #Following url /s for rejection 
        re_path(r'Comments/(?P<forkeyid>\d+)$', UserView.RejectReason.as_view(), name='RejectComments' ),
        re_path(r'multiplefiles/(?P<forkeyid>\d+)$', UserView.multiplefiles, name='multiplefiles' ),
        #pdf path
        path('GeneratePDF/',UserView.GeneratePDF,name='GeneratePDF'),
      ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
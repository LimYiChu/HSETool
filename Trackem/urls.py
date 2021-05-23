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
from Tenant.views import our_team
from rest_framework import routers

router = routers.DefaultRouter()
router.register ('ActionItems', UserView.anyView)
urlpatterns = [
      # Load excel actions, routes ,
        path ('rest/',include(router.urls)),
        
        path('upload/', login_required(UploadV.Load), name='Load' ),
        path('uploadfield/', login_required(UploadV.uploadfield), name='uploadfield' ),
        path('LoadRoutes/', login_required(UploadV.LoadRoutes), name='LoadRoutes' ),
        path('login/',auth_views.LoginView.as_view(template_name='userT/login.html'),name='login'),
        path('logout/',auth_views.LogoutView.as_view(template_name='userT/logout.html'),name='logout'),
        
        path('admin/', admin.site.urls, name='adminT'),
       # path('routes/', UserView.yourRoutes.as_view(), name='yourRoutes' ),
        #to prevent authorised view, add login_required() in front of the views, for example--> login_required(userView.mainDashboard)
        path('main/', login_required(UserView.mainDashboard), name='main' ),
        path('accounts/login/', auth_views.LoginView.as_view(template_name='userT/login.html'),name='login'),
        path('ActioneeList/', login_required(UserView.ActioneeList.as_view()), name='UserActionList' ),
                #path('UA/', UserView.yourActions.as_view(), name='UserActions' ),
        re_path(r'^(?P<id>\d+)/$', login_required(userView.getActionDetails),name='getActionsDetails'),
       # path('password_reset/', auth_views.PasswordResetView.as_view(template_name='userT/reset.html') ,name='password_reset'),
        path('routesX/', login_required(userView.getuserRoutes), name='routesX' ),
        path('main/', login_required(UserView.mainDashboard), name='main' ),
        path('', login_required(UserView.mainDashboard), name='main' ),
       
       #List path using class listview to get actionee and approver
        path('ActioneeList/', login_required(UserView.ActioneeList.as_view()), name='UserActionList' ),
        path('ApproverList/', login_required(UserView.ApproverList.as_view()), name='ApproverList' ),
        re_path(r'ApproverConfirm/(?P<id>\d+)$', login_required(UserView.ApproverConfirm.as_view()), name='ApproverConfirm' ),
        
        path('HistoryList/', login_required(UserView.HistoryList.as_view()), name='HistoryList' ),
        re_path(r'HistoryConfirm/(?P<id>\d+)$', login_required(UserView.HistoryConfirm.as_view()), name='HistoryConfirm' ),
       
        re_path(r'^(?P<id>\d+)/$', login_required(userView.getActionDetails),name='getActionsDetails'),
       
        path('routesX/', login_required(userView.getuserRoutes), name='routesX' ),
        #path('ActioneeList/<int:pk>/', userView.ActionDetails(),name='ActionsDetails'),
       
        
        #path('count/', userView.mainDashCount, name='count' ),
        #path('UA/', UserView.UserActions, name='UserActions' ),

        #Following urls are for actionee approvers updates and approvals
        path('ActioneeList/<int:pk>/update', login_required(UserView.ActioneeItemsMixin.as_view()), name='ActioneeFormMixin' ),
        path('HistoryList/<int:pk>/update', login_required(UserView.HistoryItemsMixin.as_view()), name='HistoryFormMixin' ),
        path('ActioneeList/<int:id>/', login_required(UserView.DetailActioneeItems.as_view()), name='DetailsForm' ),
        #path('ApproverList/<int:id>/approve', UserView.ApproveItems.as_view(), name='ApproveForm' ),
        path('ApproverList/<int:pk>/approve', login_required(UserView.ApproveItemsMixin.as_view()), name='ApproveFormMixin' ),

        #Following URLs are for reseting and changing password. Note that the reset password via email is yet to be set up. Right now please obtain the link in the terminal upon requesting password reset.
        path('password_change/done/',auth_views.PasswordChangeDoneView.as_view(template_name='userT/password_change_done.html'),name='password_change_done'),
        path('password_change/',auth_views.PasswordChangeView.as_view(template_name='userT/password_change.html'),name='password_change'),
        path('password_reset/done/',auth_views.PasswordResetCompleteView.as_view(template_name='userT/password_reset_done.html'),name='password_reset_done'),
        path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='userT/password_reset_confirm.html'),name='password_reset_confirm'),
        path('password_reset/',auth_views.PasswordResetView.as_view(template_name='userT/password_reset_form.html'),name='password_reset'),
        path('reset/done/',auth_views.PasswordResetCompleteView.as_view(template_name='userT/password_reset_complete.html'),name='password_reset_complete'),
        path('ContactUs/',login_required(UserView.ContactUs),name='ContactUs'),
        

        #path('ContactUs/',UserView.ContactUs,name='ContactUs'),

        #test googleapi
        path('googlecharts/',login_required(UserView.googlecharts),name='googlecharts'),
        
        #Following url /s for rejection 
        re_path(r'Comments/(?P<forkeyid>\d+)$', login_required(UserView.RejectReason.as_view()), name='RejectReason' ),
        re_path(r'multiplefiles/(?P<forkeyid>\d+)$', login_required(UserView.multiplefiles), name='multiplefiles' ),
        
        #following url for reporting
        path('actionstatus/', login_required(UserView.rptoverallStatus), name='actionstatus' ),
        path('discslice/', login_required(UserView.rptdiscSlice), name='discslice' ),
        path('rptbyuser/', login_required(UserView.rptbyUser), name='rptbyuser' ),
        #pdf path
        #path('GeneratePDF/',login_required(UserView.pdftest),name='GeneratePDF'),
        #email path
        path('ReportingTable/',login_required(UserView.ReportingTable),name='ReportingTable'),
        path('Profile/',login_required(UserView.Profile),name='Profile'),
        path('reppmt/',login_required(UserView.repPMTExcel),name='reppmt'),
        path('DisciplineBreakdown/',login_required(UserView.DisciplineBreakdown),name='DisciplineBreakdown'),
        #path('EmailReminder/',login_required(UserView.EmailReminder),name='EmailReminder'),

        path('emailreminders/',login_required(UserView.emailreminders),name='emailreminders'),
        path('EmailReminderAttachment/',login_required(UserView.EmailReminderAttachment),name='EmailReminderAttachment'),
        #StickyNote
        path('StickyNote/',login_required(UserView.StickyNote),name='StickyNote'),
        path('IndividualBreakdownByActions/',login_required(UserView.IndividualBreakdownByActions),name='IndividualBreakdownByActions'),
        path('IndividualBreakdownByUsers/',login_required(UserView.IndividualBreakdownByUsers),name='IndividualBreakdownByUsers'),
        
        #PDF close out
        path('closeoutsheet/',login_required(UserView.closeoutsheet),name='closeoutsheet'),
        path('closeoutsheet/<int:id>/print', login_required(UserView.closeoutprint), name='closeoutprint' ),
        
        #tenant
        path('our_team/', login_required(our_team), name='our_team'),

        #path('PDFtest/', UserView.PDFtest, name='PDFtest'),
      ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
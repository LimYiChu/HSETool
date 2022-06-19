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
from django.contrib.auth.decorators import login_required
from django.conf.urls.static import static
from django.conf import settings
from UploadExcel.admin import delegatedadmin_site
import debug_toolbar
from rest_framework import routers
from userT import viewsajax 

router = routers.DefaultRouter()
router.register ('ActionItems', UserView.anyView)
urlpatterns = [

        path ('rest/',include(router.urls)),
        path('__debug__/', include(debug_toolbar.urls)),
        path('delegatedadmin/', delegatedadmin_site.urls),
        path('upload/', login_required(UploadV.Load), name='Load' ),
        path('loadriskmatrix/', login_required(UploadV.loadriskmatrix), name='loadriskmatrix' ),
        path('uploadexceldf/', login_required(UploadV.uploadexceldf), name='uploadexceldf' ),
        path('LoadRoutes/', login_required(UploadV.LoadRoutes), name='LoadRoutes' ),
        
        path('admin/', admin.site.urls, name='adminT'),
        path('main/', login_required(UserView.mainDashboard), name='main' ),

        path('sidebar/', login_required(UserView.sidebar), name='sidebar' ),
        path('accounts/login/', auth_views.LoginView.as_view(template_name='userT/login.html'),name='login'),
        path('ActioneeList/', login_required(UserView.ActioneeList.as_view()), name='UserActionList' ),
        
        path('main/', login_required(UserView.mainDashboard), name='main' ),
        path('', login_required(UserView.mainDashboard), name='main' ),
       
        path('ActioneeList/', login_required(UserView.ActioneeList.as_view()), name='UserActionList' ),
        path('ApproverList/', login_required(UserView.ApproverList.as_view()), name='ApproverList' ),
        re_path(r'ApproverConfirm/(?P<id>\d+)$', login_required(UserView.ApproverConfirm.as_view()), name='ApproverConfirm' ),
        
        path('HistoryList/', login_required(UserView.HistoryList.as_view()), name='HistoryList' ),
        re_path(r'HistoryConfirm/(?P<id>\d+)$', login_required(UserView.HistoryConfirm.as_view()), name='HistoryConfirm' ),
       
        #path('HistoryList/<int:pk>/<slug:slug>/view', login_required(UserView.HistoryFormApprover.as_view()), name='HistoryFormApprover' ),
        path('HistoryList/<int:pk>/update/<actionee>', login_required(UserView.HistoryFormMixin.as_view()), name='HistoryFormMixin' ),

        #Following urls are for actionee approvers updates and approvals
        path('ActioneeList/<int:pk>/update', login_required(UserView.ActioneeItemsMixin.as_view()), name='ActioneeFormMixin' ),
        path('ActioneeList/<int:id>/', login_required(UserView.DetailActioneeItems.as_view()), name='DetailsForm' ),
        path('ApproverList/<int:pk>/approve', login_required(UserView.ApproveItemsMixin.as_view()), name='ApproveFormMixin' ),

        #Following URLs are for login, logout, reseting and changing password. 
        path('login/',auth_views.LoginView.as_view(template_name='userT/login.html'),name='login'),
        path('logout/',auth_views.LogoutView.as_view(template_name='userT/logout.html'),name='logout'),
        path('password_change/done/',auth_views.PasswordChangeDoneView.as_view(template_name='userT/password_change_done.html'),name='password_change_done'),
        path('password_change/',auth_views.PasswordChangeView.as_view(template_name='userT/password_change.html'),name='password_change'),
        path('password_reset/done/',auth_views.PasswordResetCompleteView.as_view(template_name='userT/password_reset_done.html'),name='password_reset_done'),
        path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='userT/password_reset_confirm.html'),name='password_reset_confirm'),
        path('password_reset/',auth_views.PasswordResetView.as_view(template_name='userT/password_reset_form.html'),name='password_reset'),
        path('reset/done/',auth_views.PasswordResetCompleteView.as_view(template_name='userT/password_reset_complete.html'),name='password_reset_complete'),
        path('ContactUs/',login_required(UserView.ContactUs),name='ContactUs'),

        #test googleapi
        # path('googlecharts/',login_required(UserView.googlecharts),name='googlecharts'),
        path('googlecharts88/',login_required(UserView.googlecharts88),name='googlecharts88'),

        #Following url /s for rejection 
        re_path(r'Comments/(?P<forkeyid>\d+)$', login_required(UserView.RejectReason.as_view()), name='RejectReason' ),
        re_path(r'multiplefiles/(?P<forkeyid>\d+)$', login_required(UserView.multiplefiles), name='multiplefiles' ),
        
        #20220131 ishna datatables reusable code trial
        path('datatables/', login_required(UserView.datatables), name='datatables' ),
        
        #following url for reporting
        path('actionstatus/', login_required(UserView.rptoverallStatus), name='actionstatus' ),
        path('repoverallexcel/', login_required(UserView.repoverallexcel), name='repoverallexcel' ),
        path('discslice/', login_required(UserView.rptdiscSlice), name='discslice' ),
        path('rptbyuser/', login_required(UserView.rptbyUser), name='rptbyuser' ),
        path('reppmt/',login_required(UserView.repPMTExcel),name='reppmt'),
        path('reppmt/<phase>',login_required(UserView.repPMTExcel),name='reppmtphases'),
        path('DisciplineBreakdown/',login_required(UserView.DisciplineBreakdown),name='DisciplineBreakdown'),
        path('pmtrepviewall/<int:id>/view', login_required(UserView.pmtrepviewall.as_view()), name='pmtrepviewall' ),
        
        #StickyNote
        path('StickyNote/',login_required(UserView.StickyNote),name='StickyNote'),
        path('IndividualBreakdownByActions/',login_required(UserView.IndividualBreakdownByActions),name='IndividualBreakdownByActions'),
        
        #PDF close out
        path('closeoutsheet/',login_required(UserView.closeoutsheet),name='closeoutsheet'),
        path('closeoutsheet/<phase>',login_required(UserView.closeoutsheet),name='closeoutsheetphases'),
        path('closeoutsheet/<int:id>/print', login_required(UserView.closeoutprint), name='closeoutprint' ),
        path('closeoutsheet/<path:study>/print', login_required(UserView.mergedstudycloseoutprint), name='mergedstudycloseoutprint' ),
        path('mergedcloseoutprint/', login_required(UserView.mergedcloseoutprint_update), name='mergedcloseouprint' ),
        path('stitchpdf/', login_required(UserView.stitchpdf), name='stitchpdf' ),
        
        path('addonupload/', login_required(UploadV.AddonLoad), name='addonupload' ),

        path('AllList/<int:id>/update/print', login_required(UserView.indiprint), name='indiprint' ),
        path('delegatedadmin/',login_required(UserView.delegatedadmin),name='delegatedadmin'),
        
        path('base3/', login_required(UserView.base3), name='base3' ),
        path('readsqltable/',login_required(UploadV.readsqltable), name='readsqltable'),
        
        #PMT Report Dynamic Table
        path('dynamictable/<dynamictable>', login_required(viewsajax.dynamictable), name='dynamictable'),  
     
       #PMT Report Dynamic Table Excel Download

        path('dynamicindisummexcel/<user>', login_required(viewsajax.dynamicindisummexcel), name='dynamicindisummexcel'),
        path('dynamicstudiesexcel/<study>', login_required(viewsajax.dynamicstudiesexcel), name='dynamicstudiesexcel'),
        path('dynamicstudiesdiscexcel/<study>', login_required(viewsajax.dynamicstudiesdiscexcel), name='dynamicstudiesdiscexcel'),
        path('dynamicdisciplineexcel/<path:discipline>', login_required(viewsajax.dynamicdisciplineexcel), name='dynamicdisciplineexcel'),
      ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
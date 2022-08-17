from importlib.resources import path
from .businesslogic import *
from .businesslogicQ import *
from .models import *
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponse, HttpResponseRedirect, request
from simple_history.models import HistoricalRecords
from django.views.generic import ListView, DetailView, UpdateView,TemplateView, CreateView
# import requests



class blclschecksecurity(UserPassesTestMixin):
    """
    Ying Ying 20220817
    This class is to accomodate the repeated code for test_func and handle_no_permission in mixin.
    ingroup and inroute are in boolean form. 
    Def test_func is to check whether allowing to access items in url.
    Def handle_no_permission is to handle whether user will be redirect to error page or main.
    """
    def test_func(self, ingroup, inroute, queseries=0, actioneesecondpage=False):
        if actioneesecondpage == True:
            if  (ingroup) and (inroute) and (queseries==0):
                return True
            else :
                return False
        elif actioneesecondpage == False:
            if  (ingroup) and (inroute):
                return True
            else :
                return False

    def handle_no_permission(self, approvemultipletime):    
        if approvemultipletime == True:
            return HttpResponseRedirect('/approveerror/')
        return HttpResponseRedirect('/main/')

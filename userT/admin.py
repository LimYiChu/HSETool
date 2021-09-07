from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import *
from .forms import *
from .models import CustomUser
from UploadExcel.models import ActionItems as ActionItems
from django.contrib.auth.models import Group

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# Register your models here.

# class UserAdmin(admin.ModelAdmin):
#     search_fields = ['email']
#     form = UserAdminChangeForm
#     add_form = UserAdminCreationForm

class UserAdmin2(BaseUserAdmin):
    # The forms to add and change user instances
    # form = UserAdminChangeForm
    # add_form = UserAdminCreationForm

    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    #the below is the first display page
    

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('organisation','disipline','subdisipline','designation','expiration')}),
        ('Permissions', {'fields': ('is_active','admin','staff','is_superuser','groups','user_permissions',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'fullname','password1','password2')}#this is an automated password field, dont need to code , silly took like 2 days
        ),
    )
    list_display = ('email','id','fullname','signature','designation', 'organisation','last_login')
    search_fields = ('email','designation', 'organisation')
    list_filter = ['admin']
    ordering = ('email',)

admin.site.register(CustomUser,UserAdmin2)
#admin.site.register(Group)
admin.site.register(ActionRoutes)
admin.site.register(Studies)
admin.site.register(RiskMatrix)
admin.site.register(Phases)

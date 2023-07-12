from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from accounts.forms import UserChangeForm, UserCreationsForm
from accounts.models import User


# Register your models here.
# class UserAdmin(BaseUserAdmin):
#     form = UserChangeForm
#     add_form = UserCreationsForm
#
#     list_display = ('userName', 'email', 'phoneNumber', 'type')
#
#     fieldsets = (
#         (None, {'fields': ('userName', 'email', 'phoneNumber', 'firstName', 'lastName', 'password')}),
#         ('Permission', {'fields': ('type', 'last_login',)})
#     )
#
#     add_fields = (
#         (None, {'fields': ('userName', 'phoneNumber', 'firstName', 'lastName', 'email', 'password1', 'password2  ')})
#     )
#
#     list_filter = ('userName',)
#     search_fields = ('userName',)

    # ordering = ('firstName', 'lastName')
    # filter_horizontal = ()


class UserAdmin(admin.ModelAdmin):
    # form = UserChangeForm
    # add_form = UserCreationsForm
    list_display = ('userName', 'email', 'phoneNumber', 'type')
    fieldsets = (
        (None, {'fields': ('userName', 'email', 'phoneNumber', 'firstName', 'lastName', 'password')}),
        ('Permission', {'fields': ('type', 'last_login',)})
    )
    add_fields = (
        (None, {'fields': ('userName', 'phoneNumber', 'firstName', 'lastName', 'email', 'password1', 'password2  ')})
    )
    list_filter = ('userName',)
    search_fields = ('userName',)

    def save_model(self, request, obj, form, change):
        # Check if the password field is provided
        if 'password' in form.changed_data:
            # Set the password using the set_password() method
            obj.set_password(form.cleaned_data['password'])

        # Save the user model
        super().save_model(request, obj, form, change)


admin.site.unregister(Group)
admin.site.register(User, UserAdmin)

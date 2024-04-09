from django.contrib import admin
from .models import User, UserProfile

from django.contrib.auth.admin import UserAdmin


#hidden password
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'username', 'role', 'is_active')
    ordering = ('-date_joined',) #Takecare comma(,).<class 'accounts.admin.CustomUserAdmin'>: (admin.E031) The value of 'ordering' must be a list or tuple.
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(User, CustomUserAdmin)
admin.site.register(UserProfile)


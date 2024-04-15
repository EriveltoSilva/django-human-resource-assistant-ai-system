from django.contrib import admin
from .models import Profile

# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    list_display= ['get_user']
    list_display_links =['get_user',]
    list_per_page=25    
    
    def get_user(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"
    get_user.short_description = 'Nome do Usuario'

admin.site.register(Profile, ProfileAdmin)


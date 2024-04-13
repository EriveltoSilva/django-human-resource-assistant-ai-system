from django.contrib import admin
# from .models import Profile, Area

# # Register your models here.
# class AreaAdmin(admin.ModelAdmin):
#     list_display= ['name', 'created_at', 'created_by']
#     list_display_links =['name',]
#     list_per_page=25
#     list_filter = ['name',]

# class ProfileAdmin(admin.ModelAdmin):
#     list_display= ['get_user', 'is_admin']
#     list_display_links =['get_user',]
#     list_per_page=25
#     list_filter = ['area',]    
    
#     def get_user(self, obj):
#         return f"{obj.user.first_name} {obj.user.last_name}"
#     get_user.short_description = 'Nome do Usuario'

# admin.site.register(Area, AreaAdmin)
# admin.site.register(Profile, ProfileAdmin)
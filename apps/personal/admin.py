from django.contrib import admin
from .models import *

@admin.register(AcademicInstituition)
class AcademicInstituitionAdmin(admin.ModelAdmin):
   list_display = ['id', 'name', 'created_at']
   list_display_links = ['id', 'name', 'created_at']
   list_per_page = 20

@admin.register(ProfissionalInstituition)
class ProfissionalInstituitionAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_at']
    list_display_links = ['id', 'name', 'created_at']
    list_per_page = 20

class AcademicFormationItemAdminInline(admin.TabularInline):
   model = AcademicFormationItem
   extra = 0

class ProfissionalFormationItemAdminInline(admin.TabularInline):
   model = ProfissionalFormationItem
   extra = 0

@admin.register(Formation)
class FormationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at',)
    list_display_links = ('id','user', 'created_at',)
    list_per_page = 20
    inlines = [AcademicFormationItemAdminInline, ProfissionalFormationItemAdminInline]

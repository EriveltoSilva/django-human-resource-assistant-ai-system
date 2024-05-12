from django.contrib import admin
from .models import  Vacancy, Responsability, Skill, JobType

# @admin.register(Skill)
# class SkillAdmin(admin.ModelAdmin):
#     list_display = ['id', 'title', 'created_at']
#     list_display_links = ['id', 'title', 'created_at']
#     search_fields = ['title', 'created_at']
#     list_per_page = 20

# @admin.register(Responsability)
# class ResponsabilityAdmin(admin.ModelAdmin):
#     list_display = ['id', 'title', 'created_at']
#     list_display_links = ['id', 'title', 'created_at']
#     search_fields = ['title', 'created_at']
#     list_per_page = 20

class ResponsabilityAdminInline(admin.TabularInline):
   model = Responsability
   extra = 0

class SkillAdminInline(admin.TabularInline):
   model = Skill
   extra = 0
   
@admin.register(JobType)
class JobTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'created_at']
    list_display_links = ['id', 'title', 'created_at']
    search_fields = ['title', 'created_at']
    list_per_page = 20

@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'company', 'min_wage', 'max_wage', 'created_at']
    list_display_links = ['id', 'title', 'company', 'min_wage', 'max_wage', 'created_at']
    search_fields = ['title', 'company', 'min_wage', 'max_wage']
    list_filter = ['title', 'company', 'min_wage', 'max_wage', 'description']
    list_per_page = 20
    inlines = [SkillAdminInline, ResponsabilityAdminInline]

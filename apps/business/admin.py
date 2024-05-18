""" admin config for vacancy in the django admin dashboard"""
from django.contrib import admin
from .models import JobType, Benefit, Candidate
from .models import  Vacancy, Responsibility, Skill


@admin.register(Candidate)
class CandidatesAdmin(admin.ModelAdmin):
    """register candidates in the django admin dashboard"""
    list_display = ['user', 'vacancy', 'cv','created_at']
    list_display_links = ['user', 'vacancy', 'cv','created_at']
    search_fields = ['user', 'vacancy', 'cv','created_at']
    list_per_page = 20

class BenefitAdminInline(admin.TabularInline):
    """job benefits tabular mode for admin panel"""
    model = Benefit
    extra = 0
class ResponsibilityAdminInline(admin.TabularInline):
    """job responsibility tabular mode for admin panel"""
    model = Responsibility
    extra = 0

class SkillAdminInline(admin.TabularInline):
    """job skill tabular mode for admin panel"""
    model = Skill
    extra = 0

@admin.register(JobType)
class JobTypeAdmin(admin.ModelAdmin):
    """job type class for putting in admin panel"""
    list_display = ['id', 'title', 'created_at']
    list_display_links = ['id', 'title', 'created_at']
    search_fields = ['title', 'created_at']
    list_per_page = 20

@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    """vacancy class for putting in admin panel"""
    list_display = ['id', 'title', 'company', 'min_wage', 'max_wage', 'created_at']
    list_display_links = ['id', 'title', 'company', 'min_wage', 'max_wage', 'created_at']
    search_fields = ['title', 'company', 'min_wage', 'max_wage']
    list_filter = ['title', 'company', 'min_wage', 'max_wage', 'description']
    list_per_page = 20
    inlines = [SkillAdminInline, ResponsibilityAdminInline, BenefitAdminInline]

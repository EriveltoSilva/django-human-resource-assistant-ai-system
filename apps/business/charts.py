from django.db.models import Count
from .models import Vacancy
from django.utils.timezone import now
from datetime import timedelta
from django.db.models.functions import TruncMonth
import calendar

def get_vacancies_by_month():
    vacancies = Vacancy.objects.annotate(month=TruncMonth('created_at')).values('month').annotate(total=Count('id')).order_by('month')
    labels = []
    data = []
    for vacancy in vacancies:
        month_name = calendar.month_name[vacancy['month'].month]
        labels.append(month_name)
        data.append(vacancy['total'])
    return (labels, data,)


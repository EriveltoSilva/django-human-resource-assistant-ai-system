# Generated by Django 5.0.3 on 2024-05-18 15:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0009_candidate'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vacancy',
            name='candidates',
        ),
    ]

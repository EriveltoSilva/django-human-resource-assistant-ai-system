# Generated by Django 5.0.3 on 2024-05-16 00:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0005_rename_responsability_responsibility'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vacancy',
            old_name='address',
            new_name='city',
        ),
    ]

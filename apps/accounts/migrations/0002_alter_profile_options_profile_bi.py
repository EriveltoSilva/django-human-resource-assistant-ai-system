# Generated by Django 5.0.3 on 2024-04-15 01:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profile',
            options={'ordering': ['user'], 'verbose_name_plural': 'Perfils de Usuários'},
        ),
        migrations.AddField(
            model_name='profile',
            name='bi',
            field=models.CharField(default=1, max_length=14, unique=True),
            preserve_default=False,
        ),
    ]

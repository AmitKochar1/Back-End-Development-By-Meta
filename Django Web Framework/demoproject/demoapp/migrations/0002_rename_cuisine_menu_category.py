# Generated by Django 5.0 on 2024-01-07 10:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('demoapp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='menu',
            old_name='cuisine',
            new_name='category',
        ),
    ]
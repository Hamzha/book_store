# Generated by Django 3.2.5 on 2021-08-16 17:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_user_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='Status',
            new_name='status',
        ),
    ]

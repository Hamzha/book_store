# Generated by Django 3.2.5 on 2021-08-22 08:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_auto_20210821_1518'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mode',
            old_name='mood_id',
            new_name='mode_id',
        ),
    ]
# Generated by Django 4.2.20 on 2025-04-06 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('csms', '0002_alter_schoolsettings_logo_alter_student_photo_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='class',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='class',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='class',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]

# Generated by Django 4.2.20 on 2025-03-25 16:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sms', '0006_mark_grade'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='grade',
            options={'ordering': ['-min_mark']},
        ),
        migrations.AlterModelOptions(
            name='student',
            options={'ordering': ['last_name', 'first_name']},
        ),
    ]

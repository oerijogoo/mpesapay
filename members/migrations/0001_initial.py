# Generated by Django 4.2.21 on 2025-06-02 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mem_number', models.PositiveIntegerField(default=0, editable=False, unique=True)),
                ('first_name', models.CharField(max_length=256)),
                ('last_name', models.CharField(max_length=256)),
                ('address', models.CharField(max_length=256)),
                ('contact', models.CharField(max_length=10)),
                ('status', models.CharField(choices=[('Deactivated', 'Deactivated'), ('Activated', 'Activated')], default='Activated', editable=False, max_length=11)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]

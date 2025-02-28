# Generated by Django 4.2.19 on 2025-02-28 11:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('members', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LoanAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_principal', models.PositiveIntegerField()),
                ('status', models.CharField(choices=[('Deactivated', 'Deactivated'), ('Activated', 'Activated')], default='Activated', max_length=11)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('owner', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='members.member')),
            ],
        ),
        migrations.CreateModel(
            name='LoanIssue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('loan_num', models.CharField(default='', editable=False, max_length=255, unique=True)),
                ('principal', models.PositiveIntegerField()),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Approved', 'Approved')], default='Pending', max_length=15)),
                ('delete_status', models.CharField(choices=[('False', 'False'), ('True', 'True')], default='False', editable=False, max_length=5)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='loans.loanaccount')),
            ],
        ),
        migrations.CreateModel(
            name='LoansIssue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('loan_num', models.CharField(max_length=255, unique=True)),
                ('principal', models.PositiveIntegerField()),
                ('delete_status', models.CharField(choices=[('False', 'False'), ('True', 'True')], default='False', editable=False, max_length=5)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='loans.loanaccount')),
            ],
            options={
                'verbose_name_plural': 'Loans issued',
            },
        ),
        migrations.CreateModel(
            name='LoanPayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('principal', models.PositiveIntegerField()),
                ('delete_status', models.CharField(choices=[('False', 'False'), ('True', 'True')], default='False', editable=False, max_length=5)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('loan_num', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='loans.loanissue')),
            ],
        ),
    ]

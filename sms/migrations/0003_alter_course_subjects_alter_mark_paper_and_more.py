# Generated by Django 4.2.20 on 2025-03-24 20:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sms', '0002_student_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='subjects',
            field=models.ManyToManyField(blank=True, help_text='Subjects included in this course', related_name='courses', to='sms.subject'),
        ),
        migrations.AlterField(
            model_name='mark',
            name='paper',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='marks', to='sms.paper'),
        ),
        migrations.AlterField(
            model_name='mark',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='marks', to='sms.student'),
        ),
        migrations.AlterField(
            model_name='paper',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='papers', to='sms.subject'),
        ),
        migrations.CreateModel(
            name='StudentSubjectGrade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('average', models.DecimalField(decimal_places=2, max_digits=5)),
                ('grade', models.CharField(max_length=2)),
                ('academic_year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sms.academicyear')),
                ('semester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sms.semester')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sms.student')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sms.subject')),
            ],
            options={
                'unique_together': {('student', 'subject', 'semester')},
            },
        ),
    ]

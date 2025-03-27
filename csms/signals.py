# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Enrollment, Student


@receiver(post_save, sender=Enrollment)
def update_student_current_enrollment(sender, instance, **kwargs):
    if instance.is_active:
        # Deactivate other active enrollments for this student
        Enrollment.objects.filter(
            student=instance.student,
            is_active=True
        ).exclude(pk=instance.pk).update(is_active=False)

        # Update student's current fields
        student = instance.student
        student.academic_level = instance.academic_level
        student.year_of_study = instance.year_of_study
        student.course = instance.course
        student.current_semester = instance.semester
        student.save()
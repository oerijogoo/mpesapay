from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Enrollment, StudentFeeAccount

@receiver(post_save, sender=Enrollment)
def create_student_fee_account(sender, instance, created, **kwargs):
    if created:
        StudentFeeAccount.objects.create(
            student=instance.student,
            term=instance.course.term,
            total_fees=instance.course.term.fee_amount
        )
from django.db import models

# Account status choices
ACCOUNT_STATUS_CHOICES = (
    ('Deactivated', 'Deactivated'),
    ('Activated', 'Activated'),
)


class Member(models.Model):
    mem_number = models.PositiveIntegerField(default=0, blank=False, unique=True, editable=False)
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)
    address = models.CharField(max_length=256)
    contact = models.CharField(max_length=10)
    status = models.CharField(choices=ACCOUNT_STATUS_CHOICES, default='Activated', max_length=11, editable=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.pk:  # Check if the member is new
            # Automatically assign mem_number based on the current count of members
            last_member = Member.objects.order_by('mem_number').last()
            self.mem_number = (last_member.mem_number + 1) if last_member else 1  # Start from 1

        super(Member, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


from django.db import models

# Create your models here.

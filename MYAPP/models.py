from django.db import models
from django.contrib.auth.models import User

# Models themselves were not the core cause of vulnerabilities.
# Security issues were solved in views (IDOR) and settings (cookies).

class GymBranch(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class MembershipPlan(models.Model):
    DURATION_CHOICES = [
        (1, "1 Month"),
        (3, "3 Months"),
        (6, "6 Months"),
        (12, "12 Months"),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    features = models.TextField()
    price = models.FloatField()
    duration_months = models.IntegerField(choices=DURATION_CHOICES)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Purchase(models.Model):
    # Access control now enforced securely in views.py
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(MembershipPlan, on_delete=models.CASCADE)
    branch = models.ForeignKey(GymBranch, on_delete=models.CASCADE)
    notes = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
        ],
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.plan.name}"

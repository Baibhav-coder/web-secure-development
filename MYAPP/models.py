from django.db import models
from django.contrib.auth.models import User

class GymBranch(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    city = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class MembershipPlan(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    duration_days = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - €{self.price}"


class Purchase(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(MembershipPlan, on_delete=models.CASCADE)
    branch = models.ForeignKey(GymBranch, on_delete=models.CASCADE)
    purchase_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.user.username} - {self.plan.name} ({self.status})"

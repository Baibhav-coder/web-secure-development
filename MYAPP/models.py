from django.db import models
from django.contrib.auth.models import User


# ======================================================================
# ⚠ VULNERABILITY AREA: Weak validation + missing constraints
# ======================================================================

class GymBranch(models.Model):
    name = models.CharField(max_length=100)

    # ❌ Vulnerability: No sanitisation on address or phone
    # Attackers can inject script tags or harmful markup:
    # Example: <script>alert('XSS')</script>
    address = models.TextField()

    # ❌ No validation for correct phone format
    # Impact: attacker can store fake or malformed data in the database.
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

    # ❌ Vulnerability: No sanitisation on description/features
    # These fields can store JS payloads → XSS if rendered without escaping.
    description = models.TextField()
    features = models.TextField()

    # ❌ Vulnerability: No constraints for price
    # Attackers can create:
    #   - Negative prices
    #   - Extremely large values causing overflow
    price = models.FloatField()

    duration_months = models.IntegerField(choices=DURATION_CHOICES)

    # ❌ Missing `is_active` default could cause unexpected behaviour
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Purchase(models.Model):

    # ❌ VULNERABILITY: No binding between user & access control
    # This directly contributes to the IDOR vulnerability in views.py:
    # purchase_detail(request, purchase_id)
    # An attacker can change ?purchase_id=1 and view another user’s purchases.
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    plan = models.ForeignKey(MembershipPlan, on_delete=models.CASCADE)
    branch = models.ForeignKey(GymBranch, on_delete=models.CASCADE)

    # ❌ No validation — attacker can store HTML or JS
    notes = models.TextField(blank=True, null=True)

    # ❌ No protection on status — attacker could modify it through SQLi
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

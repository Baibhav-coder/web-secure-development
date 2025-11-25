from django.contrib import admin
from .models import GymBranch, MembershipPlan, Purchase

admin.site.register(GymBranch)
admin.site.register(MembershipPlan)
admin.site.register(Purchase)

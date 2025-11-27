from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .forms import RegisterForm
from .models import GymBranch, MembershipPlan, Purchase


# ======================================================================
# HOME PAGE (SAFE VIEW — READ-ONLY CONTENT)
# ======================================================================
# This function only retrieves public data and renders it.
# No user-controlled input is processed here.
def home(request):
    plans = MembershipPlan.objects.filter(is_active=True)
    branches = GymBranch.objects.all()

    return render(request, 'MYAPP/home.html', {
        'plans': plans,
        'branches': branches,
    })


# ======================================================================
# USER REGISTRATION (SECURE IMPLEMENTATION)
# ======================================================================
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            # ----------------------------------------------------------
            # ✅ SECURITY FIX: PASSWORD HASHING (PBKDF2)
            # ----------------------------------------------------------
            # Previously: Password was stored in plaintext.
            #
            # Now:
            #   • set_password() hashes the password using PBKDF2
            #   • Prevents credential disclosure if database leaks
            #   • Meets OWASP & NIST password storage requirements
            #
            # Result:
            #   Stored passwords cannot be reversed or read by attackers.
            # ----------------------------------------------------------
            user.set_password(form.cleaned_data['password'])
            user.save()

            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('home')

    else:
        form = RegisterForm()

    return render(request, 'MYAPP/register.html', {'form': form})


# ======================================================================
# USER LOGIN (SQL INJECTION FULLY REMOVED)
# ======================================================================
def login_view(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # ----------------------------------------------------------
        # ✅ SECURITY FIX: SAFE AUTHENTICATION
        # ----------------------------------------------------------
        # Previously:
        #   Raw SQL was being constructed with user input → SQL Injection.
        #
        # Now:
        #   authenticate():
        #     • Uses parameterized queries internally
        #     • Compares hashed passwords safely
        #     • Eliminates possibility of SQL injection
        #
        # Result:
        #   No attacker can bypass login using `' OR '1'='1`.
        # ----------------------------------------------------------
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'MYAPP/login.html')


# ======================================================================
# USER LOGOUT (SECURE BY DESIGN)
# ======================================================================
def logout_view(request):
    logout(request)
    messages.info(request, "Logged out successfully")
    return redirect('home')


# ======================================================================
# MEMBERSHIP PLANS LIST (SAFE VIEW)
# ======================================================================
@login_required
def plans_view(request):
    plans = MembershipPlan.objects.filter(is_active=True)
    return render(request, 'MYAPP/plans.html', {'plans': plans})


# ======================================================================
# PURCHASE MEMBERSHIP (SAFE — VALIDATES PLAN & BRANCH IDs)
# ======================================================================
@login_required
def purchase_plan(request, plan_id):

    # ----------------------------------------------------------
    # Secure access:
    #   get_object_or_404 ensures:
    #     • Only valid plans are processed
    #     • Invalid IDs cannot cause unwanted behavior
    # ----------------------------------------------------------
    plan = get_object_or_404(MembershipPlan, id=plan_id)
    branches = GymBranch.objects.all()

    if request.method == 'POST':
        branch_id = request.POST.get('branch')

        # Again, safely validate branch ownership.
        branch = get_object_or_404(GymBranch, id=branch_id)

        Purchase.objects.create(
            user=request.user,
            plan=plan,
            branch=branch,
        )
        return redirect('my_purchases')

    return render(request, 'MYAPP/purchase.html', {
        'plan': plan,
        'branches': branches
    })


# ======================================================================
# VIEW USER’S OWN PURCHASES (SAFE ACCESS CONTROL)
# ======================================================================
@login_required
def my_purchases(request):
    # Only show purchases belonging to the logged-in user
    purchases = Purchase.objects.filter(user=request.user)
    return render(request, 'MYAPP/my_purchases.html', {'purchases': purchases})


# ======================================================================
# PURCHASE DETAIL (IDOR FULLY FIXED)
# ======================================================================
@login_required
def purchase_detail(request, purchase_id):

    # ----------------------------------------------------------
    # ✅ SECURITY FIX: IDOR (Insecure Direct Object Reference)
    # ----------------------------------------------------------
    # Previously:
    #   Attacker could change "purchase_id" in URL and view another
    #   user's purchase.
    #
    # Now:
    #   get_object_or_404(Purchase, id=purchase_id, user=request.user)
    #   enforces:
    #     • The record must belong to the logged-in user
    #     • If not → 404 Not Found (no information leak)
    #
    # Result:
    #   Cross-user data exposure is impossible.
    # ----------------------------------------------------------
    purchase = get_object_or_404(
        Purchase,
        id=purchase_id,
        user=request.user
    )

    return render(request, 'MYAPP/purchase_detail.html', {'purchase': purchase})

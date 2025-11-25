from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.db import connection
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .forms import RegisterForm
from .models import GymBranch, MembershipPlan, Purchase


# ======================================================================
# HOME PAGE (DISPLAYS PLANS + BRANCHES)
# ======================================================================
def home(request):
    # Home page is safe — just returns data to the template.
    plans = MembershipPlan.objects.filter(is_active=True)
    branches = GymBranch.objects.all()

    return render(request, 'MYAPP/home.html', {
        'plans': plans,
        'branches': branches,
    })


# ======================================================================
# USER REGISTRATION (INTENTIONALLY VULNERABLE)
# ======================================================================
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            # ==========================================================
            # 🚨 VULNERABILITY #2: PLAIN TEXT PASSWORD STORAGE
            # ----------------------------------------------------------
            # Instead of hashing passwords (Django uses PBKDF2 by default),
            # this code stores the password in clear text.
            #
            # IMPACT:
            #   • If database is leaked → All real passwords exposed
            #   • Administrator can see user passwords
            #   • Violates every security standard (GDPR, NIST, OWASP)
            #
            # REAL FIX WOULD BE: user.set_password(...)
            # ==========================================================
            user.password = form.cleaned_data['password']  # ❌ insecure
            user.save()

            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('home')
    else:
        form = RegisterForm()

    return render(request, 'MYAPP/register.html', {'form': form})


# ======================================================================
# USER LOGIN (INTENTIONALLY VULNERABLE)
# ======================================================================
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # ==========================================================
        # 🚨 VULNERABILITY #1: SQL INJECTION
        # ----------------------------------------------------------
        # This raw SQL query directly injects user input without
        # sanitization. An attacker can:
        #
        #   • Bypass login using → ' OR '1'='1
        #   • Dump password table using UNION SELECT
        #   • Log in as admin without password
        #
        # This is one of the most severe OWASP vulnerabilities.
        #
        # REAL FIX WOULD BE: use Django's authenticate()
        # ==========================================================
        sql = f"SELECT id, username FROM auth_user WHERE username='{username}' AND password='{password}'"

        with connection.cursor() as cursor:
            cursor.execute(sql)  # ❌ Executes user-controlled SQL
            user_data = cursor.fetchone()

        if user_data:
            user = User.objects.get(id=user_data[0])
            login(request, user)
            messages.success(request, "Login successful (RAW SQL used).")
            return redirect('home')
        else:
            messages.error(request, "Invalid credentials entered.")

    return render(request, 'MYAPP/login.html')


# ======================================================================
# USER LOGOUT
# ======================================================================
def logout_view(request):
    logout(request)
    messages.info(request, "Logged out successfully")
    return redirect('home')


# ======================================================================
# MEMBERSHIP PLANS LIST
# ======================================================================
@login_required
def plans_view(request):
    # This displays all available membership plans.
    plans = MembershipPlan.objects.filter(is_active=True)
    return render(request, 'MYAPP/plans.html', {'plans': plans})


# ======================================================================
# PURCHASE MEMBERSHIP (SAFE)
# ======================================================================
@login_required
def purchase_plan(request, plan_id):
    plan = MembershipPlan.objects.get(id=plan_id)
    branches = GymBranch.objects.all()

    if request.method == 'POST':
        branch_id = request.POST.get('branch')
        branch = GymBranch.objects.get(id=branch_id)

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
# VIEW USER’S OWN PURCHASES (SAFE)
# ======================================================================
@login_required
def my_purchases(request):
    purchases = Purchase.objects.filter(user=request.user)
    return render(request, 'MYAPP/my_purchases.html', {'purchases': purchases})


# ======================================================================
# PURCHASE DETAIL (INTENTIONALLY VULNERABLE)
# ======================================================================
@login_required
def purchase_detail(request, purchase_id):

    # ==========================================================
    # 🚨 VULNERABILITY #3: IDOR (Insecure Direct Object Reference)
    # ----------------------------------------------------------
    # Problem:
    #   This line fetches ANY purchase based only on purchase_id.
    #
    #   Attack:
    #       If user A changes the URL:
    #           /purchase-detail/5/
    #       They can view user B’s order.
    #
    # WHY IT'S DANGEROUS:
    #   • Leaks personal billing data
    #   • Cross-user data exposure
    #   • Violates access control rules
    #
    # REAL FIX WOULD BE:
    #   Purchase.objects.get(id=purchase_id, user=request.user)
    # ==========================================================
    purchase = Purchase.objects.get(id=purchase_id)  # ❌ no ownership check

    return render(request, 'MYAPP/purchase_detail.html', {'purchase': purchase})

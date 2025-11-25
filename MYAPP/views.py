from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.db import connection
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .forms import RegisterForm
from .models import GymBranch, MembershipPlan, Purchase


# -------------------------------
# HOME PAGE (SHOW PLANS + BRANCHES)
# -------------------------------
def home(request):
    plans = MembershipPlan.objects.filter(is_active=True)
    branches = GymBranch.objects.all()

    return render(request, 'MYAPP/home.html', {
        'plans': plans,
        'branches': branches,
    })


# -------------------------------
# AUTHENTICATION (VULNERABLE)
# -------------------------------
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            # ❌ Vulnerability: storing password in plain text
            user.password = form.cleaned_data['password']
            user.save()

            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('home')
    else:
        form = RegisterForm()

    return render(request, 'MYAPP/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # ❌ Vulnerable RAW SQL (SQL Injection)
        sql = f"SELECT id, username FROM auth_user WHERE username='{username}' AND password='{password}'"

        with connection.cursor() as cursor:
            cursor.execute(sql)
            user_data = cursor.fetchone()

        if user_data:
            user = User.objects.get(id=user_data[0])
            login(request, user)
            messages.success(request, "Login successful (RAW SQL).")
            return redirect('home')
        else:
            messages.error(request, "Invalid credentials")

    return render(request, 'MYAPP/login.html')


def logout_view(request):
    logout(request)
    messages.info(request, "Logged out successfully")
    return redirect('home')


# -------------------------------
# MEMBERSHIP PLANS + PURCHASE FLOW
# -------------------------------
@login_required
def plans_view(request):
    plans = MembershipPlan.objects.filter(is_active=True)
    return render(request, 'MYAPP/plans.html', {'plans': plans})


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


@login_required
def my_purchases(request):
    purchases = Purchase.objects.filter(user=request.user)
    return render(request, 'MYAPP/my_purchases.html', {'purchases': purchases})


@login_required
def purchase_detail(request, purchase_id):
    # ❌ Vulnerability: IDOR (NO permission check)
    purchase = Purchase.objects.get(id=purchase_id)

    return render(request, 'MYAPP/purchase_detail.html', {'purchase': purchase})


# --------------------------------------------------------
# VULNERABILITY #3 : PLAIN-TEXT PASSWORD LEAK ENDPOINT
# --------------------------------------------------------
def leak_users(request):
    """
    ⚠ EXPOSES ALL USER ACCOUNTS (ID, USERNAME, PASSWORD, EMAIL)
    This is intentionally insecure for your project demo.
    """

    with connection.cursor() as cursor:
        cursor.execute("SELECT id, username, password, email FROM auth_user")
        rows = cursor.fetchall()

    return render(request, 'MYAPP/leak.html', {"rows": rows})

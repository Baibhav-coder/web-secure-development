from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .forms import RegisterForm
from .models import GymBranch, MembershipPlan, Purchase


# ======================================================================
# HOME PAGE (SAFE)
# ======================================================================
def home(request):
    plans = MembershipPlan.objects.filter(is_active=True)
    branches = GymBranch.objects.all()

    return render(request, 'MYAPP/home.html', {
        'plans': plans,
        'branches': branches,
    })


# ======================================================================
# USER REGISTRATION (SECURE)
# ======================================================================
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            # ----------------------------------------------------------
            # FIXED: PASSWORD HASHING
            # ----------------------------------------------------------
            # Django automatically hashes passwords using PBKDF2.
            # This prevents plaintext password disclosure risk.
            user.set_password(form.cleaned_data['password'])
            user.save()

            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('home')
    else:
        form = RegisterForm()

    return render(request, 'MYAPP/register.html', {'form': form})


# ======================================================================
# USER LOGIN (SECURE)
# ======================================================================
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # ----------------------------------------------------------
        # FIXED: SQL INJECTION REMOVED
        # ----------------------------------------------------------
        # authenticate() safely checks credentials using hashing,
        # parameterized queries, and Django's auth backend.
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'MYAPP/login.html')


# ======================================================================
# LOGOUT
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
    plans = MembershipPlan.objects.filter(is_active=True)
    return render(request, 'MYAPP/plans.html', {'plans': plans})


# ======================================================================
# PURCHASE MEMBERSHIP (SAFE)
# ======================================================================
@login_required
def purchase_plan(request, plan_id):
    plan = get_object_or_404(MembershipPlan, id=plan_id)
    branches = GymBranch.objects.all()

    if request.method == 'POST':
        branch_id = request.POST.get('branch')
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
# VIEW USER’S OWN PURCHASES
# ======================================================================
@login_required
def my_purchases(request):
    purchases = Purchase.objects.filter(user=request.user)
    return render(request, 'MYAPP/my_purchases.html', {'purchases': purchases})


# ======================================================================
# PURCHASE DETAIL (SECURE — IDOR FIXED)
# ======================================================================
@login_required
def purchase_detail(request, purchase_id):

    # ----------------------------------------------------------
    # FIXED: IDOR VULNERABILITY
    # ----------------------------------------------------------
    # We now enforce ownership:
    # Only the user who made the purchase can access it.
    # If not owned → 404 Not Found.
    # ----------------------------------------------------------
    purchase = get_object_or_404(
        Purchase,
        id=purchase_id,
        user=request.user
    )

    return render(request, 'MYAPP/purchase_detail.html', {'purchase': purchase})

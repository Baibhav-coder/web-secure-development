from django.urls import path
from . import views

urlpatterns = [
    # Home
    path('', views.home, name='home'),

    # Authentication
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Plans + Purchase
    path('plans/', views.plans_view, name='plans'),
    path('purchase/<int:plan_id>/', views.purchase_plan, name='purchase_plan'),
    path('my-purchases/', views.my_purchases, name='my_purchases'),
    path('purchase-detail/<int:purchase_id>/', views.purchase_detail, name='purchase_detail'),
]

from django.urls import path
from . import views

urlpatterns = [
    # --- Public Pages ---
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('doctors/', views.doctors_view, name='doctors'),

    # --- Authentication (The new parts) ---
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),

    # --- Protected Pages (Require Login) ---
    path('reservation/', views.reservation, name='reservation'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # ... existing paths ...
    path('reservation/', views.reservation, name='reservation'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # ADD THIS NEW LINE:
    path('profile/', views.profile, name='profile'),
]
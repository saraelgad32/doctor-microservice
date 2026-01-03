from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Appointment
import grpc
from . import doctor_pb2, doctor_pb2_grpc

# Auth imports
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages

# --- Helper to call gRPC ---
# UPDATED: Now accepts an optional neighborhood_filter
def get_doctors_from_service(neighborhood_filter=None):
    try:
        # Tries to connect to your running microservice
        channel = grpc.insecure_channel('localhost:50051')
        stub = doctor_pb2_grpc.DoctorControllerStub(channel)
        
        # We pass the filter (or empty string if None)
        req = doctor_pb2.DoctorRequest(neighborhood=neighborhood_filter or "")
        
        response = stub.GetDoctors(req)
        channel.close()
        return response.doctors
    except Exception as e:
        print(f"gRPC Error: {e}")
        return []

# --- Standard Page Views ---

def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

# UPDATED: Handles the filter logic
def doctors_view(request):
    # 1. Get the selected neighborhood from the URL
    selected_hood = request.GET.get('neighborhood')
    
    # 2. Get the filtered list of doctors to display
    doctors = get_doctors_from_service(selected_hood)

    # 3. Get ALL doctors just to build the unique list of neighborhoods for the dropdown
    all_doctors = get_doctors_from_service()
    neighborhoods = sorted(list(set([d.neighborhood for d in all_doctors if d.neighborhood and d.neighborhood != "Unknown"])))

    context = {
        'doctors': doctors,
        'neighborhoods': neighborhoods,
        'selected_hood': selected_hood
    }
    return render(request, 'doctors.html', context)

# --- AUTHENTICATION VIEWS ---

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log them in immediately after signing up
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            # Retrieve the user object from the form
            user = form.get_user()
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('index')

# --- APP LOGIC ---

@login_required(login_url='login')
def reservation(request):
    # Pass 'None' to get all doctors for the dropdown
    doctors = get_doctors_from_service()
    
    if request.method == 'POST':
        doctor_name = request.POST.get('doctor_name')
        
        specialty = "General"
        for doc in doctors:
            if doc.name == doctor_name:
                specialty = doc.specialty
                break
                
        Appointment.objects.create(
            user=request.user,
            doctor_name=doctor_name,
            specialty=specialty,
            date=request.POST.get('date'),
            time=request.POST.get('time'),
            reason=request.POST.get('reason')
        )
        return redirect('dashboard')
    
    return render(request, 'reservation.html', {'doctors': doctors})

@login_required(login_url='login')
def dashboard(request):
    appointments = Appointment.objects.filter(user=request.user).order_by('-date')
    return render(request, 'dashboard.html', {'appointments': appointments})

def profile(request):
    return render(request, 'profile.html')
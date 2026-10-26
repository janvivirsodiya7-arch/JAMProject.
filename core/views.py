from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from doctor_app.models import *
from patient_app.models import *
from appointments.models import *
from .forms import *
from django.contrib.auth import login


# Create your views here.
def home(request):
    doctors = Doctor.objects.all()
    return render(request, "home.html", {"doctors": doctors})
        

from django.shortcuts import render


@login_required(login_url="login")
def dashboard(request):
    appointments = Appointment.objects.none()
    doctors = Doctor.objects.none()
    patients = Patient.objects.none()

    if request.user.is_superuser:
        appointments = Appointment.objects.all()
        doctors = Doctor.objects.all()
        patients = Patient.objects.all()

    elif request.user.user_type == "doctor":
        appointments = Appointment.objects.filter(
            doctor__user=request.user
        )
        doctors = Doctor.objects.filter(user=request.user)

        patient_list = appointments.values_list(
            "patient_id", flat=True
        )
        patients = Patient.objects.filter(id__in=patient_list)

    elif request.user.user_type == "patient":
        appointments = Appointment.objects.filter(
            patient__user=request.user
        )

    context = {
        "appointments": appointments,
        "doctors": doctors,
        "patients": patients,
    }

    return render(request, "dashboard.html", context)



def register(request, type):
    user_type = type

    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.user_type = user_type

            # IMPORTANT: If RegisterForm doesn't already hash the password,
            # uncomment this and use the password field from the form.
            # user.set_password(form.cleaned_data["password"])

            user.save()
            # Automatically authenticate the newly registered user
            login(request, user)
            print(f"🚀 Registration successful as {user.user_type}: {user.email}")
            messages.success(
                request,
                f"🚀 Registration successful as {user.user_type}: {user.email}"
            )
            if user_type == "patient":
                url = "/patient/create/"
            elif user_type == "doctor":
                url = "/doctor/create/"
            else:
                url = "/dashboard/"
            # Redirect wherever you want after registration
            return redirect(url)

        else:
            print("Form validation failed!")
            print(form.errors)

            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(
                        request,
                        f"{field.capitalize()}: {error}"
                    )

    else:
        form = RegisterForm()

    return render(
        request,
        "registration/register.html",
        {
            "form": form,
            "page_title": "Register"
        }
    )

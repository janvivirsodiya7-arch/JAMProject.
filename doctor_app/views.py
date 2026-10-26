from django.contrib import messages
import random
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator
from .filters import DoctorFilter
from .forms import DoctorForm
from .models import Doctor
from core.models import CoreUser
from appointments.models import Appointment


@login_required
def doctor_list(request):
    doctors = Doctor.objects.select_related("user").order_by("-created_at")

    print("🐓Doctors - ", doctors.count())
    
    queryset = doctors
    doctor_filter = DoctorFilter(request.GET,queryset=queryset,)

    paginator = Paginator(doctor_filter.qs,10,)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    query_params = request.GET.copy()
    if "page" in query_params:
        query_params.pop("page")

    context = {
        "filter": doctor_filter,
        "doctors": page_obj,
        "page_obj": page_obj,
        "query_params": query_params.urlencode(),
    }

    return render(
        request,
        "doctor_app/doctor_list.html",
        context
    )



@login_required
def doctor_detail(request, pk):
    doctor = get_object_or_404(
        Doctor.objects.select_related("user"),
        pk=pk
    )

    return render(
        request,
        "doctor_app/doctor_detail.html",
        {"doctor": doctor}
    )


@login_required
def doctor_create(request):
    if request.method == "POST":
        form = DoctorForm(request=request, data=request.POST)

        if form.is_valid():
            doctor = form.save(commit=False)
            d_id = f"DR-{random.randint(1000000, 9999999)}"
            doctor.doctor_id = d_id
            doctor.save()

            messages.success(
                request,
                "Doctor created successfully!"
            )

            return redirect("doctor:doctor_detail", pk=doctor.pk)

        else:
            messages.error(
                request,
                "Please correct the errors below."
            )

    else:
        form = DoctorForm(request=request)

    return render(
        request,
        "doctor_app/doctor_form.html",
        {"form": form}
    )


@login_required
def doctor_update(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)

    if request.method == "POST":
        form = DoctorForm(
            request=request,
            data=request.POST,
            instance=doctor
        )

        if form.is_valid():
            doctor = form.save()

            messages.success(
                request,
                "Doctor updated successfully!"
            )

            return redirect("doctor:doctor_detail", pk=doctor.pk)

        else:
            messages.error(
                request,
                "Please correct the errors below."
            )

    else:
        form = DoctorForm(instance=doctor, request=request)

    return render(
        request,
        "doctor_app/doctor_form.html",
        {
            "form": form,
            "doctor": doctor,
        }
    )



@login_required
def doctor_delete(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)

    if request.method == "POST":
        doctor.delete()

        messages.success(
            request,
            "Doctor deleted successfully!"
        )

        return redirect("doctor:doctor_list")

    return render(
        request,
        "doctor_app/doctor_confirm_delete.html",
        {"doctor": doctor}
    )
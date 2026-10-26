import random
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator
from .filters import PatientFilter
from .forms import PatientForm
from .models import Patient
from core.models import CoreUser
from appointments.models import Appointment
from django.contrib import messages


@login_required
def patient_list(request):
    patients = Patient.objects.none()
    if request.user.user_type in [
        CoreUser.UserType.NURSE,
        CoreUser.UserType.RECEPTIONIST]:
        print("Nurse/receptionist check passed")
        patients = Patient.objects.select_related("user").order_by("-created_at")

    elif request.user.user_type == "doctor":
        print("Doctor check passed")
        appointments = Appointment.objects.filter(doctor__user=request.user)
        patient_list = appointments.values_list("patient_id",flat=True)
        patients = Patient.objects.filter(id__in=patient_list).select_related("user").order_by("-created_at")

    elif request.user.is_superuser:
            print("Super check passed")
            patients = Patient.objects.all().select_related("user").order_by("-created_at")

    print("🐓Patients - ", patients.count())

    queryset = patients
    patient_filter = PatientFilter(request.GET,queryset=queryset,)

    paginator = Paginator(patient_filter.qs,10,)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    query_params = request.GET.copy()
    if "page" in query_params:
        query_params.pop("page")

    context = {
        "filter": patient_filter,
        "patients": page_obj,
        "page_obj": page_obj,
        "query_params": query_params.urlencode(),
    }

    return render(
        request,
        "patient_app/patient_list.html",
        context
    )



@login_required
def patient_create(request):
    if request.method == "POST":
        form = PatientForm(request=request, data=request.POST)

        if form.is_valid():
            patient = form.save(commit=False)
            p_id = f"P-{random.randint(1000000, 9999999)}"
            patient.patient_id = p_id
            patient.save()

            messages.success(
                request,
                "Patient created successfully!"
            )

            return redirect("patient:patient_detail", pk=patient.pk)

        else:
            messages.error(
                request,
                "Please correct the errors below."
            )

    else:
        form = PatientForm(request=request)

    return render(
        request,
        "patient_app/patient_form.html",
        {"form": form}
    )


@login_required
def patient_update(request, pk):
    patient = get_object_or_404(Patient, pk=pk)

    if request.method == "POST":
        form = PatientForm(request.POST, instance=patient)

        if form.is_valid():
            patient = form.save()

            messages.success(
                request,
                "Patient updated successfully!"
            )

            return redirect("patient:patient_detail", pk=patient.pk)

        else:
            messages.error(
                request,
                "Please correct the errors below."
            )

    else:
        form = PatientForm(instance=patient)

    return render(
        request,
        "patient_app/patient_form.html",
        {
            "form": form,
            "patient": patient,
        }
    )



@login_required
def patient_detail(request, pk):
    patient = get_object_or_404(
        Patient.objects.select_related("user"),
        pk=pk
    )

    return render(
        request,
        "patient_app/patient_detail.html",
        {"patient": patient}
    )





@login_required
def patient_delete(request, pk):
    patient = get_object_or_404(Patient, pk=pk)

    if request.method == "POST":
        patient.delete()

        messages.success(
            request,
            "Patient deleted successfully!"
        )

        return redirect("patient:patient_list")

    return render(
        request,
        "patient_app/patient_confirm_delete.html",
        {"patient": patient}
    )




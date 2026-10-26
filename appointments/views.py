
import random
from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .filters import AppointmentFilter
from .forms import AppointmentForm, TreatmentForm
from .models import Appointment, Treatment


def get_user_appointments(user):
    """
    Return only appointments the logged-in user is allowed to access.
    Superusers can access all appointments.
    Patients can access their own appointments.
    Doctors can access appointments assigned to them.
    """
    appointments = Appointment.objects.select_related(
        "patient__user",
        "doctor__user",
    )

    if user.is_superuser:
        return appointments

    user_type = getattr(user, "user_type", None)

    if user_type == "patient":
        return appointments.filter(patient__user=user)

    if user_type == "doctor":
        return appointments.filter(doctor__user=user)

    # Any other account type receives no appointment access.
    return appointments.none()


def can_manage_treatment(user, appointment):
    """Only the assigned doctor or a superuser can manage treatment."""
    if user.is_superuser:
        return True

    return (
        getattr(user, "user_type", None) == "doctor"
        and appointment.doctor.user_id == user.pk
    )


@login_required
def appointment_list(request):
    today = datetime.today().date()

    # Update today's appointment statuses.
    todays_appointments = Appointment.objects.filter(date=today)

    for appointment in todays_appointments:
        if appointment.status == "booked":
            appointment.status = "today"
            appointment.save(update_fields=["status"])

    # Start with appointments the current user is allowed to access.
    appointments = get_user_appointments(request.user).filter(
        date__gte=today,
    ).order_by("date", "time")

    appointment_filter = AppointmentFilter(
        request.GET,
        queryset=appointments,
    )

    paginator = Paginator(appointment_filter.qs, 25)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    query_params = request.GET.copy()
    query_params.pop("page", None)

    context = {
        "filter": appointment_filter,
        "appointments": page_obj,
        "page_obj": page_obj,
        "query_params": query_params.urlencode(),
    }

    return render(
        request,
        "appointments/appointment_list.html",
        context,
    )


@login_required
def appointment_create(request):
    if request.method == "POST":
        form = AppointmentForm(
            request=request,
            data=request.POST,
        )

        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.status = "booked"

            appointment.appointment_id = (
                f"A-{datetime.now().strftime('%y%m%d')}-"
                f"{random.randint(1000000, 9999999)}"
            )

            appointment.save()

            messages.success(
                request,
                "Appointment successfully created!",
            )

            return redirect(
                "appointment:appointment_detail",
                pk=appointment.pk,
            )

    else:
        form = AppointmentForm(request=request)

    return render(
        request,
        "appointments/appointment_form.html",
        {"form": form},
    )


@login_required
def appointment_update(request, pk):
    appointment = get_user_appointments(request.user).filter(
        pk=pk,
    ).first()

    if appointment is None:
        messages.error(
            request,
            "You are not authorized to access this appointment.",
        )
        return redirect("appointment:appointment_list")

    if request.method == "POST":
        form = AppointmentForm(
            data=request.POST,
            instance=appointment,
            request=request,
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Appointment updated successfully!",
            )

            return redirect(
                "appointment:appointment_detail",
                pk=appointment.pk,
            )

    else:
        form = AppointmentForm(
            instance=appointment,
            request=request,
        )

    return render(
        request,
        "appointments/appointment_form.html",
        {
            "form": form,
            "appointment": appointment,
        },
    )


@login_required
def appointment_detail(request, pk):
    # Do not retrieve an appointment outside this user's permitted records.
    appointment = get_user_appointments(request.user).filter(
        pk=pk,
    ).first()

    if appointment is None:
        messages.error(
            request,
            "You are not authorized to access this appointment.",
        )
        return redirect("appointment:appointment_list")

    treatment = getattr(appointment, "treatment", None)
    user_can_manage_treatment = can_manage_treatment(
        request.user,
        appointment,
    )

    edit_treatment = (
        request.GET.get("edit_treatment") == "1"
        or request.POST.get("editing_treatment") == "1"
    )

    if request.method == "POST":
        # Block patients and any unassigned doctor from changing treatment.
        if not user_can_manage_treatment:
            messages.error(
                request,
                "You are not allowed to add or edit treatment details.",
            )
            return redirect(
                "appointment:appointment_detail",
                pk=appointment.pk,
            )

        is_update = treatment is not None

        if is_update:
            treatment_form = TreatmentForm(
                request.POST,
                instance=treatment,
            )
        else:
            treatment_form = TreatmentForm(request.POST)

        if treatment_form.is_valid():
            treatment = treatment_form.save(commit=False)
            treatment.appointment = appointment
            treatment.save()

            appointment.status = "attended"
            appointment.save(update_fields=["status"])

            if is_update:
                messages.success(
                    request,
                    "Treatment details updated successfully!",
                )
            else:
                messages.success(
                    request,
                    "Treatment details saved successfully!",
                )

            return redirect(
                "appointment:appointment_detail",
                pk=appointment.pk,
            )

    else:
        if not user_can_manage_treatment:
            # Do not show an editable treatment form to patients.
            treatment_form = None
            edit_treatment = False
        elif treatment:
            treatment_form = TreatmentForm(instance=treatment)
        else:
            treatment_form = TreatmentForm()

    return render(
        request,
        "appointments/appointment_detail.html",
        {
            "appointment": appointment,
            "treatment": treatment,
            "treatment_form": treatment_form,
            "edit_treatment": edit_treatment,
            "can_manage_treatment": user_can_manage_treatment,
        },
    )


@login_required
def appointment_delete(request, pk):
    appointment = get_user_appointments(request.user).filter(
        pk=pk,
    ).first()

    if appointment is None:
        messages.error(
            request,
            "You are not authorized to access this appointment.",
        )
        return redirect("appointment:appointment_list")

    if request.method == "POST":
        appointment.delete()

        messages.success(
            request,
            "Appointment deleted successfully.",
        )

        return redirect("appointment:appointment_list")

    return render(
        request,
        "appointments/appointment_confirm_delete.html",
        {"appointment": appointment},
    )


@login_required
def treatment_list(request):
    treatments = Treatment.objects.filter(
        appointment__isnull=False,
    ).select_related(
        "appointment",
        "appointment__patient__user",
        "appointment__doctor__user",
    )

    if request.user.is_superuser:
        pass

    elif getattr(request.user, "user_type", None) == "patient":
        treatments = treatments.filter(
            appointment__patient__user=request.user,
        )

    elif getattr(request.user, "user_type", None) == "doctor":
        treatments = treatments.filter(
            appointment__doctor__user=request.user,
        )

    else:
        treatments = treatments.none()

    treatments = treatments.order_by(
        "-appointment__date",
        "-appointment__time",
    )

    return render(
        request,
        "appointments/treatment_list.html",
        {"treatments": treatments},
    )


from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit

from .models import Appointment, Treatment
from core.models import CoreUser
from patient_app.models import Patient
from doctor_app.models import Doctor


from datetime import datetime, time, timedelta


def generate_time_slots(
    start_time=time(10, 0),
    end_time=time(20, 0),
):
    slots = []
    current = datetime.combine(
        datetime.today(),
        start_time
    )
    end = datetime.combine(
        datetime.today(),
        end_time
    )

    while current <= end:
        value = current.time().strftime("%H:%M")
        label = current.strftime("%I:%M %p").lstrip("0")
        slots.append((value, label))
        current += timedelta(minutes=30)
    # returns time slots as string
    return slots




class AppointmentForm(forms.ModelForm):
    patient = forms.ModelChoiceField(
        queryset=Patient.objects.none(),
        widget=forms.Select(attrs={
            "class": "form-select",
            "id": "id_patient",
        })
    )

    doctor = forms.ModelChoiceField(
        queryset=Doctor.objects.none(),
        widget=forms.Select(attrs={
            "class": "form-select",
            "id": "id_doctor",
        })
    )
    time = forms.ChoiceField(choices=[])


    class Meta:
        model = Appointment
        fields = [
            "patient",
            "doctor",
            "date",
            "time",
        ]

        widgets = {
            "patient": forms.Select(attrs={
                "class": "form-select",
            }),

            "doctor": forms.Select(attrs={
                "class": "form-select",
            }),

            "date": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date",
            }),

            "time": forms.TimeInput(attrs={
                "class": "form-control",
                "type": "time",
            }),
        }


    def clean(self):
        cleaned_data = super().clean()

        doctor = cleaned_data.get("doctor")
        date = cleaned_data.get("date")
        time_value = cleaned_data.get("time")

        if doctor and date and time_value:
            # ChoiceField returns a string, so convert it to time.
            appointment_time = datetime.strptime(
                time_value,
                "%H:%M"
            ).time()

            qs = Appointment.objects.filter(
                doctor=doctor,
                date=date,
                time=appointment_time,
            )

            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)

            if qs.exists():
                self.add_error(
                    "time",
                    "Sorry ! this appointment time slot is already "
                    "booked by other patient."
                )

        return cleaned_data

    def save(self, commit=True):
        appointment = super().save(commit=False)

        # ChoiceField gives us a string such as "10:30".
        if self.cleaned_data.get("time"):
            appointment.time = datetime.strptime(
                self.cleaned_data["time"],
                "%H:%M"
            ).time()

        if commit:
            appointment.save()
        return appointment



    def __init__(self, *args, request=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.request = request
        if request is not None:

            # Superuser, Nurse and Receptionist
            # can select a Doctor user.
            if (
                request.user.is_superuser
                or request.user.user_type in [
                    CoreUser.UserType.NURSE,
                    CoreUser.UserType.RECEPTIONIST,
                ]):
                self.fields["patient"].queryset = Patient.objects.select_related("user")
                self.fields["doctor"].queryset = Doctor.objects.select_related("user")
            elif request.user.user_type == "doctor":
                self.fields["patient"].queryset = Patient.objects.select_related("user")
                self.fields["doctor"].queryset = Doctor.objects.filter(user=request.user)
                self.fields["doctor"].initial = Doctor.objects.get(user=request.user)
                self.fields["doctor"].disabled = True

            elif request.user.user_type=="patient":
                print("PAtient User - ", request.user)
                patient = Patient.objects.get(user=request.user)

                self.fields["doctor"].queryset = Doctor.objects.select_related("user")
                self.fields["patient"].queryset = Patient.objects.filter(pk=patient.pk)
                self.fields["patient"].initial = patient
                self.fields["patient"].disabled = True


        slots = generate_time_slots()

        doctor = self.data.get("doctor")
        date = self.data.get("date")

        if doctor and date:
            booked_times = Appointment.objects.filter(
                doctor_id=doctor,
                date=date,
            )

            # Don't consider the current appointment when editing.
            if self.instance.pk:
                booked_times = booked_times.exclude(
                    pk=self.instance.pk
                )

            booked_times = {
                appointment.time.strftime("%H:%M")
                for appointment in booked_times
            }

            slots = [
                (value, label)
                for value, label in slots
                if value not in booked_times
            ]

        self.fields["time"].choices = slots
        
        # Crispy Form Layout
        self.helper = FormHelper()
        self.helper.form_method = "post"

        self.helper.layout = Layout(
            Row(
                Column(
                    "patient",
                    css_class="col-md-6"
                ),
                Column(
                    "doctor",
                    css_class="col-md-6"
                ),
            ),

            Row(
                Column(
                    "date",
                    css_class="col-md-6"
                ),
                Column(
                    "time",
                    css_class="col-md-6"
                ),
            ),

            Submit(
                "submit",
                "Book Appointment",
                css_class="btn btn-primary"
            ),
        )





class TreatmentForm(forms.ModelForm):

    class Meta:
        model = Treatment
        fields = [
            "symptoms",
            "diagnosis",
            "treatment",
            "prescription",
        ]

        widgets = {
            "symptoms": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Patient symptoms...",
            }),

            "diagnosis": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Diagnosis...",
            }),

            "treatment": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Treatment details...",
            }),

            "prescription": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Prescription...",
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_tag = False

        self.helper.layout = Layout(
            "symptoms",
            "diagnosis",
            "treatment",
            "prescription",
            Submit(
                "submit",
                "Submit",
                css_class="btn btn-primary"
            ),
        )




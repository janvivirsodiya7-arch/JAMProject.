from django.core.exceptions import ValidationError
from django.db import models
from patient_app.models import Patient
from doctor_app.models import Doctor

class Appointment(models.Model):
    class StatusType(models.TextChoices):
        BOOKED = "booked", "Booked"
        TODAY = "today", "Today"
        ATTENDED = "attended", "Attended"
        CANCELLED = "cancelled", "Cancelled"
        MISSED = "missed", "Missed"

    appointment_id = models.CharField(max_length=50, unique=True)
    patient = models.ForeignKey(Patient,on_delete=models.CASCADE,related_name="appointments")
    doctor = models.ForeignKey(Doctor,on_delete=models.CASCADE,related_name="doctor_appointments")
    status = models.CharField(max_length=20, choices=StatusType.choices, default=StatusType.BOOKED)

    date = models.DateField()
    time = models.TimeField()
    consultation_fee = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=500
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date", "-time"]

        constraints = [
            models.UniqueConstraint(
                fields=["doctor", "date", "time"],
                name="unique_doctor_date_time"
            )
        ]

    # @property
    # def status_badge_class(self):
    #     return {
    #         StatusType.BOOKED: "bg-info",
    #         StatusType.ATTENDED: "bg-success",
    #         StatusType.CANCELLED: "bg-danger",
    #         StatusType.MISSED: "bg-secondary",
    #         StatusType.TODAY: "bg-warning",
    #     }.get(self.status, "bg-secondary")

    




    def __str__(self):
        return f"{self.appointment_id} - {self.patient}"

    def clean(self):
        super().clean()

        if self.doctor_id and self.date and self.time:
            qs = Appointment.objects.filter(
                doctor=self.doctor,
                date=self.date,
                time=self.time,
            )

            # When editing an existing appointment, don't compare
            # the appointment against itself.
            if self.pk:
                qs = qs.exclude(pk=self.pk)

            if qs.exists():
                raise ValidationError({
                    "time": (
                        "Sorry ! this appointment time is already "
                        "booked by other patient."
                    )
                })






class Treatment(models.Model):
    class Disease(models.TextChoices):
        DIABETES = "diabetes", "Diabetes"
        HYPERTENSION = "hypertension", "Hypertension"
        ASTHMA = "asthma", "Asthma"
        HEART_DISEASE = "heart_disease", "Heart Disease"
        KIDNEY_DISEASE = "kidney_disease", "Kidney Disease"
        LIVER_DISEASE = "liver_disease", "Liver Disease"
        CANCER = "cancer", "Cancer"
        ARTHRITIS = "arthritis", "Arthritis"
        THYROID = "thyroid", "Thyroid Disease"
        COPD = "copd", "COPD"
        OTHER = "other", "Other"

    class Allergy(models.TextChoices):
        PENICILLIN = "penicillin", "Penicillin"
        ASPIRIN = "aspirin", "Aspirin"
        SULFA = "sulfa", "Sulfa Drugs"
        LATEX = "latex", "Latex"
        PEANUTS = "peanuts", "Peanuts"
        TREE_NUTS = "tree_nuts", "Tree Nuts"
        MILK = "milk", "Milk"
        EGGS = "eggs", "Eggs"
        SHELLFISH = "shellfish", "Shellfish"
        OTHER = "other", "Other"

    appointment = models.OneToOneField("Appointment", on_delete=models.SET_NULL, null=True, blank=True, related_name="treatment")
    height = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="cm")
    weight = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, help_text="kg")
    bmi = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    diseases = models.TextField(null=True,blank=True)
    allergies = models.TextField(null=True,blank=True)
    medications = models.TextField(null=True,blank=True)
    surgeries = models.TextField(null=True,blank=True)
    family_history = models.TextField(null=True,blank=True)

    has_diabetes = models.BooleanField(default=False)

    systolic_bp = models.PositiveIntegerField(null=True, blank=True, help_text="mmHg")
    diastolic_bp = models.PositiveIntegerField(null=True, blank=True, help_text="mmHg")

    blood_glucose = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    hba1c = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)

    heart_rate = models.PositiveIntegerField(null=True, blank=True, help_text="BPM")
    respiratory_rate = models.PositiveIntegerField(null=True, blank=True, help_text="breaths/min")
    oxygen_saturation = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="SpO2 %")
    temperature = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True, help_text="°C")

    smoking = models.BooleanField(default=False)
    alcohol = models.BooleanField(default=False)

    symptoms = models.TextField(blank=True)
    diagnosis = models.TextField(blank=True)
    treatment = models.TextField(blank=True)
    prescription = models.TextField(blank=True)

    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



from django.db import models
from core.models import CoreUser

class Patient(models.Model):
    user = models.OneToOneField(CoreUser, on_delete=models.CASCADE, related_name="patient")
    patient_id = models.CharField(max_length=50, null=True, blank=True)
    insurance_id = models.CharField(max_length=50, null=True,blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    blood_group = models.CharField(max_length=200, null=True)
    emergency_contact = models.CharField(max_length=15, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
            return f"Patient: - {self.user.get_full_name() or self.user.email}"
    


    




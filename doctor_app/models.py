from django.db import models
from core.models import CoreUser

# Create your models here.

class Doctor(models.Model):
    class SpecialistType(models.TextChoices):
        GENERAL = "general", "General Physician"
        SURGEON = "surgeon", "Surgeon"
        PHYSICIAN = "physician", "Physician"
        THERAPIST = "therapist", "Therapist"
        CARDIOLOGIST = "cardiologist", "Cardiologist"
        NEUROLOGIST = "neurologist", "Neurologist"
        PEDIATRICIAN = "pediatrician", "Pediatrician"
        DERMATOLOGIST = "dermatologist", "Dermatologist"
        ORTHOPEDIC = "orthopedic", "Orthopedic Surgeon"
        OTHER = "other", "Other"

     
    user = models.OneToOneField(CoreUser, on_delete=models.CASCADE, related_name="doctor")
    doctor_id = models.CharField(max_length=50, null=True, blank=True) 
    qualification = models.CharField(max_length=255, blank=True)
    specialist = models.CharField(max_length=50, choices=SpecialistType.choices, default=SpecialistType.GENERAL)
    experience = models.PositiveIntegerField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Dr: {self.user.get_full_name() or self.user.email}"

from decimal import Decimal, ROUND_HALF_UP

from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    Layout,
    Row,
    Column,
    Field,
    Div,
    HTML,
    Submit,
)

from .models import Treatment


class TreatmentForm(forms.ModelForm):

    diseases = forms.MultipleChoiceField(
        label="Known Diseases",
        choices=Treatment.Disease.choices,
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

    allergies = forms.MultipleChoiceField(
        label="Known Allergies",
        choices=Treatment.Allergy.choices,
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Treatment

        fields = [
            "appointment",

            # Measurements
            "height",
            "weight",
            "bmi",

            # Medical history
            "diseases",
            "allergies",
            "medications",
            "surgeries",
            "family_history",

            # Diabetes
            "has_diabetes",
            "blood_glucose",
            "hba1c",

            # Vital signs
            "systolic_bp",
            "diastolic_bp",
            "heart_rate",
            "respiratory_rate",
            "oxygen_saturation",
            "temperature",

            # Lifestyle
            "smoking",
            "alcohol",

            # Clinical assessment
            "symptoms",
            "diagnosis",
            "treatment",
            "prescription",
            "notes",
        ]

        widgets = {
            "height": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Height in cm",
                    "step": "0.01",
                    "min": "0",
                    "data-bmi-height": "true",
                }
            ),

            "weight": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Weight in kg",
                    "step": "0.01",
                    "min": "0",
                    "data-bmi-weight": "true",
                }
            ),

            "bmi": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Automatically calculated",
                    "readonly": True,
                    "tabindex": "-1",
                }
            ),

            "medications": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": (
                        "List current medications, dosage and frequency..."
                    ),
                }
            ),

            "surgeries": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": (
                        "Previous surgeries or procedures..."
                    ),
                }
            ),

            "family_history": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": (
                        "Relevant family medical history..."
                    ),
                }
            ),

            "symptoms": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "placeholder": (
                        "Describe the patient's presenting symptoms..."
                    ),
                }
            ),

            "diagnosis": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "placeholder": (
                        "Clinical diagnosis / assessment..."
                    ),
                }
            ),

            "treatment": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "placeholder": (
                        "Treatment plan and recommendations..."
                    ),
                }
            ),

            "prescription": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 6,
                    "placeholder": (
                        "Medication, dosage, frequency and instructions..."
                    ),
                }
            ),

            "notes": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Additional clinical notes...",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["appointment"].required = False

        # Existing JSONField values are already lists.
        if self.instance and self.instance.pk:
            self.initial["diseases"] = self.instance.diseases or []
            self.initial["allergies"] = self.instance.allergies or []

        # -----------------------------------------------------
        # Crispy Forms
        # -----------------------------------------------------

        self.helper = FormHelper()

        self.helper.form_method = "post"
        self.helper.form_class = "treatment-form"

        self.helper.layout = Layout(

            # =================================================
            # APPOINTMENT
            # =================================================

            Div(
                HTML(
                    """
                    <div class="section-header">
                        <div class="section-icon">
                            <i class="bi bi-calendar-check"></i>
                        </div>
                        <div>
                            <h5>Appointment</h5>
                            <p>Select the appointment associated with this treatment.</p>
                        </div>
                    </div>
                    """
                ),

                Field(
                    "appointment",
                    css_class="form-select",
                ),

                css_class="card shadow-sm mb-4",
            ),

            # =================================================
            # PHYSICAL MEASUREMENTS
            # =================================================

            Div(
                HTML(
                    """
                    <div class="section-header">
                        <div class="section-icon">
                            <i class="bi bi-rulers"></i>
                        </div>
                        <div>
                            <h5>Physical Measurements</h5>
                            <p>Record the patient's height, weight and BMI.</p>
                        </div>
                    </div>
                    """
                ),

                Row(
                    Column(
                        Field("height"),
                        HTML(
                            '<small class="text-muted">'
                            'Centimeters (cm)'
                            "</small>"
                        ),
                        css_class="col-md-4",
                    ),

                    Column(
                        Field("weight"),
                        HTML(
                            '<small class="text-muted">'
                            'Kilograms (kg)'
                            "</small>"
                        ),
                        css_class="col-md-4",
                    ),

                    Column(
                        Field("bmi"),
                        HTML(
                            '<small class="text-muted">'
                            'Calculated automatically'
                            "</small>"
                        ),
                        css_class="col-md-4",
                    ),
                ),

                css_class="card shadow-sm mb-4 p-4",
            ),

            # =================================================
            # MEDICAL HISTORY
            # =================================================

            Div(
                HTML(
                    """
                    <div class="section-header">
                        <div class="section-icon">
                            <i class="bi bi-clipboard2-pulse"></i>
                        </div>
                        <div>
                            <h5>Medical History</h5>
                            <p>Record existing conditions and allergies.</p>
                        </div>
                    </div>

                    <h6 class="field-section-title">
                        Known Diseases
                    </h6>
                    """
                ),

                Field(
                    "diseases",
                    css_class="choice-grid",
                ),

                HTML(
                    """
                    <hr class="my-4">

                    <h6 class="field-section-title">
                        Known Allergies
                    </h6>
                    """
                ),

                Field(
                    "allergies",
                    css_class="choice-grid",
                ),

                css_class="card shadow-sm mb-4 p-4",
            ),

            # =================================================
            # MEDICAL BACKGROUND
            # =================================================

            Div(
                HTML(
                    """
                    <div class="section-header">
                        <div class="section-icon">
                            <i class="bi bi-file-medical"></i>
                        </div>
                        <div>
                            <h5>Medical Background</h5>
                            <p>Additional medical history and background.</p>
                        </div>
                    </div>
                    """
                ),

                Field("medications"),
                Field("surgeries"),
                Field("family_history"),

                css_class="card shadow-sm mb-4 p-4",
            ),

            # =================================================
            # VITAL SIGNS
            # =================================================

            Div(
                HTML(
                    """
                    <div class="section-header">
                        <div class="section-icon">
                            <i class="bi bi-heart-pulse"></i>
                        </div>
                        <div>
                            <h5>Vital Signs</h5>
                            <p>Record the patient's current vital signs.</p>
                        </div>
                    </div>
                    """
                ),

                Row(
                    Column(
                        Field("systolic_bp"),
                        css_class="col-md-6",
                    ),

                    Column(
                        Field("diastolic_bp"),
                        css_class="col-md-6",
                    ),
                ),

                Row(
                    Column(
                        Field("heart_rate"),
                        css_class="col-md-3",
                    ),

                    Column(
                        Field("respiratory_rate"),
                        css_class="col-md-3",
                    ),

                    Column(
                        Field("oxygen_saturation"),
                        css_class="col-md-3",
                    ),

                    Column(
                        Field("temperature"),
                        css_class="col-md-3",
                    ),
                ),

                css_class="card shadow-sm mb-4 p-4",
            ),

            # =================================================
            # DIABETES
            # =================================================

            Div(
                HTML(
                    """
                    <div class="section-header">
                        <div class="section-icon">
                            <i class="bi bi-droplet-half"></i>
                        </div>
                        <div>
                            <h5>Diabetes & Blood Glucose</h5>
                            <p>Record diabetes status and glucose measurements.</p>
                        </div>
                    </div>
                    """
                ),

                Field(
                    "has_diabetes",
                    wrapper_class="form-check mb-4",
                ),

                Row(
                    Column(
                        Field("blood_glucose"),
                        css_class="col-md-6",
                    ),

                    Column(
                        Field("hba1c"),
                        css_class="col-md-6",
                    ),
                ),

                css_class="card shadow-sm mb-4 p-4",
            ),

            # =================================================
            # LIFESTYLE
            # =================================================

            Div(
                HTML(
                    """
                    <div class="section-header">
                        <div class="section-icon">
                            <i class="bi bi-person"></i>
                        </div>
                        <div>
                            <h5>Lifestyle</h5>
                            <p>Record relevant lifestyle information.</p>
                        </div>
                    </div>
                    """
                ),

                Row(
                    Column(
                        Field(
                            "smoking",
                            wrapper_class="form-check",
                        ),
                        css_class="col-md-6",
                    ),

                    Column(
                        Field(
                            "alcohol",
                            wrapper_class="form-check",
                        ),
                        css_class="col-md-6",
                    ),
                ),

                css_class="card shadow-sm mb-4 p-4",
            ),

            # =================================================
            # CLINICAL ASSESSMENT
            # =================================================

            Div(
                HTML(
                    """
                    <div class="section-header">
                        <div class="section-icon">
                            <i class="bi bi-activity"></i>
                        </div>
                        <div>
                            <h5>Clinical Assessment</h5>
                            <p>Document symptoms and clinical findings.</p>
                        </div>
                    </div>
                    """
                ),

                Field("symptoms"),
                Field("diagnosis"),

                css_class="card shadow-sm mb-4 p-4",
            ),

            # =================================================
            # TREATMENT
            # =================================================

            Div(
                HTML(
                    """
                    <div class="section-header">
                        <div class="section-icon">
                            <i class="bi bi-prescription2"></i>
                        </div>
                        <div>
                            <h5>Treatment & Prescription</h5>
                            <p>Document the treatment plan and prescription.</p>
                        </div>
                    </div>
                    """
                ),

                Field("treatment"),
                Field("prescription"),

                css_class="card shadow-sm mb-4 p-4",
            ),

            # =================================================
            # NOTES
            # =================================================

            Div(
                HTML(
                    """
                    <div class="section-header">
                        <div class="section-icon">
                            <i class="bi bi-journal-text"></i>
                        </div>
                        <div>
                            <h5>Additional Notes</h5>
                            <p>Add any other relevant clinical information.</p>
                        </div>
                    </div>
                    """
                ),

                Field("notes"),

                css_class="card shadow-sm mb-4 p-4",
            ),

            # =================================================
            # ACTIONS
            # =================================================

            Div(
                Submit(
                    "submit",
                    "Save Treatment",
                    css_class="btn btn-primary px-4",
                ),

                HTML(
                    """
                    <a href="javascript:history.back()"
                       class="btn btn-outline-secondary px-4 ms-2">
                        Cancel
                    </a>
                    """
                ),

                css_class="d-flex justify-content-end gap-2 mb-5",
            ),
        )

    # =========================================================
    # Validation
    # =========================================================

    def clean(self):
        cleaned_data = super().clean()

        height = cleaned_data.get("height")
        weight = cleaned_data.get("weight")

        # Calculate BMI from height and weight.
        if height and weight:
            if height <= 0:
                self.add_error(
                    "height",
                    "Height must be greater than zero.",
                )

            if weight <= 0:
                self.add_error(
                    "weight",
                    "Weight must be greater than zero.",
                )

            if height > 0 and weight > 0:
                height_m = height / Decimal("100")

                bmi = weight / (height_m ** 2)

                cleaned_data["bmi"] = bmi.quantize(
                    Decimal("0.01"),
                    rounding=ROUND_HALF_UP,
                )

        else:
            cleaned_data["bmi"] = None

        # Blood pressure sanity checks
        systolic = cleaned_data.get("systolic_bp")
        diastolic = cleaned_data.get("diastolic_bp")

        if systolic and diastolic and systolic <= diastolic:
            self.add_error(
                "systolic_bp",
                "Systolic BP should be greater than diastolic BP.",
            )

        # SpO2
        oxygen = cleaned_data.get("oxygen_saturation")

        if oxygen is not None and not (
            Decimal("0") <= oxygen <= Decimal("100")
        ):
            self.add_error(
                "oxygen_saturation",
                "Oxygen saturation must be between 0 and 100%.",
            )

        # HbA1c
        hba1c = cleaned_data.get("hba1c")

        if hba1c is not None and hba1c < 0:
            self.add_error(
                "hba1c",
                "HbA1c cannot be negative.",
            )

        return cleaned_data



from .models import Patient
from core.models import CoreUser
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    Layout,
    Row,
    Column,
    Field,
    Fieldset,
    Div,
    HTML,
    Submit,
)



class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = [
            "user",
            "insurance_id",
            "age",
            "blood_group",
            "emergency_contact",
        ]

    def __init__(self, *args, request=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.request = request

        if request is not None:
            if request.user.is_superuser or request.user.user_type in [
                    CoreUser.UserType.DOCTOR, 
                    CoreUser.UserType.NURSE,
                    CoreUser.UserType.RECEPTIONIST]:
                # Superuser can select the patient user.
                self.fields["user"].queryset = CoreUser.objects.filter(
                    user_type="patient"
                ).order_by("first_name", "last_name", "email")

            elif request.user.user_type == CoreUser.UserType.PATIENT:
                # Patient can only use their own CoreUser.
                self.fields["user"].queryset = CoreUser.objects.filter(
                    pk=request.user.pk
                )

                self.fields["user"].initial = request.user

                # Don't allow the patient to change the user.
                self.fields["user"].disabled = True

        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_class = "row g-3"

        self.helper.layout = Layout(

            # User
            Div(
                Row(
                    Column(
                        "user",
                        css_class="col-md-12",
                    ),
                ),
                css_class="card-body",
            ),

            # Patient information
            Div(
                HTML('<h5 class="mb-3">Patient Information</h5>'),

                Row(
                    Column(
                        "age",
                        css_class="col-md-6",
                    ),
                    Column(
                        "blood_group",
                        css_class="col-md-6",
                    ),
                ),

                Row(
                    Column(
                        "emergency_contact",
                        css_class="col-md-6",
                    ),
                    Column(
                        "insurance_id",
                        css_class="col-md-6",
                    ),
                ),

                css_class="card-body border-top",
            ),

            # Buttons
            Div(
                Submit(
                    "submit",
                    "Save Patient",
                    css_class="btn btn-primary",
                ),
                HTML(
                    '<a href="{% url \'patient:patient_list\' %}" '
                    'class="btn btn-secondary ms-2">Cancel</a>'
                ),
                css_class="card-footer bg-white text-end",
            ),
        )




"""
class PatientForm1(forms.ModelForm):

    diseases = forms.MultipleChoiceField(
        choices=Patient.Disease.choices,
        required=False,
        widget=forms.SelectMultiple(attrs={
            "class": "form-select",
            "size": 5,
        }),
    )

    allergies = forms.MultipleChoiceField(
        choices=Patient.Allergy.choices,
        required=False,
        widget=forms.SelectMultiple(attrs={
            "class": "form-select",
            "size": 5,
        }),
    )

    class Meta:
        model = Patient
        fields = [
            "user",
            "age",
            "height",
            "weight",
            "bmi",
            "diseases",
            "allergies",
            "medications",
            "surgeries",
            "family_history",
            "has_diabetes",
            "systolic_bp",
            "diastolic_bp",
            "blood_glucose",
            "hba1c",
            "heart_rate",
            "respiratory_rate",
            "oxygen_saturation",
            "temperature",
            "smoking",
            "alcohol",
            "notes",
        ]

        widgets = {
            "age": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Age",
                "min": 0,
                "max": 150,
            }),

            "height": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Height in cm",
                "step": "0.01",
                "min": 0,
            }),

            "weight": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Weight in kg",
                "step": "0.01",
                "min": 0,
            }),

            "bmi": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "BMI",
                "step": "0.01",
                "min": 0,
                "readonly": "readonly",
            }),

            "medications": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Current medications...",
            }),

            "surgeries": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Previous surgeries...",
            }),

            "family_history": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Relevant family medical history...",
            }),

            "systolic_bp": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Systolic",
                "min": 0,
            }),

            "diastolic_bp": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Diastolic",
                "min": 0,
            }),

            "blood_glucose": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Blood glucose",
                "step": "0.01",
                "min": 0,
            }),

            "hba1c": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "HbA1c %",
                "step": "0.01",
                "min": 0,
            }),

            "heart_rate": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "BPM",
                "min": 0,
            }),

            "respiratory_rate": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Breaths/min",
                "min": 0,
            }),

            "oxygen_saturation": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "SpO2 %",
                "step": "0.01",
                "min": 0,
                "max": 100,
            }),

            "temperature": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Temperature °C",
                "step": "0.1",
            }),

            "notes": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Additional notes...",
            }),

            "user": forms.Select(attrs={
                "class": "form-select",
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            self.initial["diseases"] = [
                x.strip() for x in self.instance.diseases.split(",") if x.strip()
            ]
            self.initial["allergies"] = [
                x.strip() for x in self.instance.allergies.split(",") if x.strip()
            ]


        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_class = "row g-3"

        self.helper.layout = Layout(

            # Patient
            Div(
                HTML('<h5 class="mb-3">Patient Information</h5>'),
                Row(
                    Column("user", css_class="col-md-12"),
                ),
                css_class="card-body",
            ),

            # Physical information
            Div(
                HTML('<h5 class="mb-3">Physical Information</h5>'),
                Row(
                    Column("age", css_class="col-md-4"),
                    Column("height", css_class="col-md-4"),
                    Column("weight", css_class="col-md-4"),
                ),
                Row(
                    Column("bmi", css_class="col-md-4"),
                ),
                css_class="card-body border-top",
            ),

            # Medical history
            Div(
                HTML('<h5 class="mb-3">Medical History</h5>'),
                Row(
                    Column("diseases", css_class="col-md-6"),
                    Column("allergies", css_class="col-md-6"),
                ),
                Row(
                    Column("medications", css_class="col-md-4"),
                    Column("surgeries", css_class="col-md-4"),
                    Column("family_history", css_class="col-md-4"),
                ),
                css_class="card-body border-top",
            ),

            # Diabetes / Blood pressure
            Div(
                HTML('<h5 class="mb-3">Diabetes & Blood Pressure</h5>'),
                Row(
                    Column("has_diabetes", css_class="col-md-4"),
                    Column("systolic_bp", css_class="col-md-4"),
                    Column("diastolic_bp", css_class="col-md-4"),
                ),
                Row(
                    Column("blood_glucose", css_class="col-md-6"),
                    Column("hba1c", css_class="col-md-6"),
                ),
                css_class="card-body border-top",
            ),

            # Vitals
            Div(
                HTML('<h5 class="mb-3">Vital Signs</h5>'),
                Row(
                    Column("heart_rate", css_class="col-md-4"),
                    Column("respiratory_rate", css_class="col-md-4"),
                    Column("oxygen_saturation", css_class="col-md-4"),
                ),
                Row(
                    Column("temperature", css_class="col-md-4"),
                ),
                css_class="card-body border-top",
            ),

            # Lifestyle
            Div(
                HTML('<h5 class="mb-3">Lifestyle</h5>'),
                Row(
                    Column("smoking", css_class="col-md-6"),
                    Column("alcohol", css_class="col-md-6"),
                ),
                css_class="card-body border-top",
            ),

            # Notes
            Div(
                HTML('<h5 class="mb-3">Additional Notes</h5>'),
                "notes",
                css_class="card-body border-top",
            ),

            # Buttons
            Div(
                Submit(
                    "submit",
                    "Save Patient",
                    css_class="btn btn-primary",
                ),
                HTML(
                    '<a href="{% url \'patient_list\' %}" '
                    'class="btn btn-secondary ms-2">Cancel</a>'
                ),
                css_class="card-footer bg-white text-end",
            ),
        )

    def clean_diseases(self):
        diseases = self.cleaned_data.get("diseases", [])
        return ",".join(diseases)

    def clean_allergies(self):
        allergies = self.cleaned_data.get("allergies", [])
        return ",".join(allergies)

    def clean(self):
        cleaned_data = super().clean()

        height = cleaned_data.get("height")
        weight = cleaned_data.get("weight")

        if height and weight and height > 0:
            height_m = float(height) / 100
            bmi = float(weight) / (height_m ** 2)
            cleaned_data["bmi"] = round(bmi, 2)

        return cleaned_data


"""

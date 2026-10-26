from .models import Doctor
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



class DoctorForm(forms.ModelForm):

    class Meta:
        model = Doctor
        fields = [
            "user",
            "qualification",
            "specialist",
            "experience",
            "bio",
        ]

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
                ]
            ):
                self.fields["user"].queryset = (
                    CoreUser.objects
                    .filter(
                        user_type=CoreUser.UserType.DOCTOR,
                    )
                    .order_by(
                        "first_name",
                        "last_name",
                        "email",
                    )
                )

            # Doctor can only use their own CoreUser.
            elif request.user.user_type == CoreUser.UserType.DOCTOR:

                self.fields["user"].queryset = CoreUser.objects.filter(
                    pk=request.user.pk
                )

                self.fields["user"].initial = request.user

                self.fields["user"].disabled = True

        # -------------------------------------------------
        # Crispy Forms
        # -------------------------------------------------

        self.helper = FormHelper()

        self.helper.form_method = "post"
        self.helper.form_class = "row g-3"

        self.helper.layout = Layout(

            # -------------------------------------------------
            # Doctor / User
            # -------------------------------------------------

            Div(
                HTML(
                    '<h5 class="mb-3">Doctor Account</h5>'
                ),

                Row(
                    Column(
                        "user",
                        css_class="col-md-12",
                    ),
                ),

                css_class="card-body",
            ),

            # -------------------------------------------------
            # Professional Information
            # -------------------------------------------------

            Div(
                HTML(
                    '<h5 class="mb-3">Professional Information</h5>'
                ),

                Row(
                    Column(
                        "qualification",
                        css_class="col-md-8",
                    ),

                    Column(
                        "specialist",
                        css_class="col-md-4",
                    ),
                ),

                Row(
                    Column(
                        "experience",
                        css_class="col-md-6",
                    ),
                ),

                css_class="card-body border-top",
            ),

            # -------------------------------------------------
            # Biography
            # -------------------------------------------------

            Div(
                HTML(
                    '<h5 class="mb-3">Biography</h5>'
                ),

                Row(
                    Column(
                        "bio",
                        css_class="col-md-12",
                    ),
                ),

                css_class="card-body border-top",
            ),

            # -------------------------------------------------
            # Buttons
            # -------------------------------------------------

            Div(
                Submit(
                    "submit",
                    "Save",
                    css_class="btn btn-primary",
                ),

                HTML(
                    '<a href="{% url \'doctor:doctor_list\' %}" '
                    'class="btn btn-secondary ms-2">'
                    'Cancel'
                    '</a>'
                ),

                css_class="card-footer bg-white text-end",
            ),
        )

    def save(self, commit=True):
        doctor = super().save(commit=False)

        # A doctor is never allowed to change
        # the CoreUser associated with their Doctor profile.
        if (
            self.request
            and not self.request.user.is_superuser
            and self.request.user.user_type == CoreUser.UserType.DOCTOR
        ):
            doctor.user = self.request.user

        if commit:
            doctor.save()

        return doctor

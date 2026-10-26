from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Row, Column, Submit
from .models import CoreUser

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CoreUser
        fields = ["first_name", "last_name", "email", "password", "password2",
            'dob','gender','mobile','street','address','city','country','postcode',
            'profile_pic']

        widgets = {"address": forms.Textarea(attrs={"rows": 4}),
                   'dob': forms.DateInput(attrs={'type': 'date'}),
                   }

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("password") != cleaned_data.get("password2"):
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            Fieldset("Account",
            Row(Column("first_name", css_class="col-md-6"), 
                Column("last_name", css_class="col-md-6"), 
            ),
            Row(Column("email", css_class="col-md-8"), 
                Column('mobile', css_class='col-md-4'),  
            ),
            Row(Column("password", css_class="col-md-6"), 
                Column("password2", css_class="col-md-6"), 
            ),
            ),
            Fieldset("Information",
                    Row(
                        Column('dob', css_class='col-md-6'),
                        Column('gender', css_class='col-md-6'),
                    ),
                    Row(
                        Column('profile_pic', css_class='col-md-12'),
                    ),
                    Row(
                        Column('address', css_class='col-md-12'),
                    ),
                    Row(
                        Column('street', css_class='col-md-3'),
                        Column('city', css_class='col-md-3'),
                        Column('country', css_class='col-md-3'),
                        Column('postcode', css_class='col-md-3'),
                    ),
            ),
            Submit("submit", "Register", css_class="btn btn-primary"),
        )


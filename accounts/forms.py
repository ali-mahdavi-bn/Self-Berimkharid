from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.validators import MinLengthValidator
from django.utils.translation import gettext as _
from rest_framework.exceptions import ValidationError

from accounts.models import User


class UserCreationsForm(forms.ModelForm):
    password1 = forms.CharField(label='password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='confirm password', widget=forms.PasswordInput)
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text="Your password must contain at least 8 characters, including both letters and numbers.",
        validators=[
            # Validate password length
            MinLengthValidator(8, message="Your password must be at least 8 characters long."),
        ]
    )

    class Meta:
        model = User
        fields = ('email', 'firstName', 'lastName', 'phoneNumber', 'userName', 'password1', 'password2')

    def clean_phoneNumber(self):
        phoneNumber = self.cleaned_data.get('phoneNumber')
        if not phoneNumber.isdigit():
            raise ValidationError("Please enter a valid phone number with only numeric characters.")
        if len(phoneNumber) != 11:
            raise ValidationError("Please enter a valid 10-digit phone number.")
        return phoneNumber

    def clean_firstName(self):
        firstName = self.cleaned_data.get('firstName')
        if not firstName.isalpha():
            raise ValidationError("Please enter a valid first name with only alphabetical characters.")

            # Check if the first name is at least 2 characters long
        if len(firstName) < 2:
            raise ValidationError("Please enter a valid first name with at least 2 characters.")

            # Check if the first name is not too long
        if len(firstName) > 50:
            raise ValidationError("Please enter a valid first name that is not longer than 30 characters.")

        return firstName

    def clean_lastName(self):
        lastName = self.cleaned_data.get('lastName')
        if not lastName.isalpha():
            raise ValidationError("Please enter a valid last name with only alphabetical characters.")

        # Check if the last name is at least 2 characters long
        if len(lastName) < 2:
            raise ValidationError("Please enter a valid last name with at least 2 characters.")

            # Check if the last name is not too long
        if len(lastName) > 50:
            raise ValidationError("Please enter a valid last name that is not longer than 30 characters.")

        return lastName

    def clean_password1(self):
        password = self.cleaned_data.get('password1')

        # Check if the password contains the user's first name
        firstName = self.cleaned_data.get('firstName')
        if firstName and firstName.lower() in password.lower():
            raise ValidationError("Your password cannot contain your first name.")

        # Check if the password contains the user's last name
        lastName = self.cleaned_data.get('lastName')
        if lastName and lastName.lower() in password.lower():
            raise ValidationError("Your password cannot contain your last name.")

    def clean_password2(self):
        cd = self.cleaned_data

        if cd['password1'] and cd['password2'] and cd['password1'] != cd['password2']:
            raise ValidationError('password dont match')

        return cd['password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])

        if commit:
            user.save()


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        help_text="you can change password using <a href=\" ../password/ \">this form</a>")

    class Meta:
        model = User
        fields = ('email', 'firstName', 'lastName', 'phoneNumber', 'password', 'userName')

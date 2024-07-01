from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import (
    PasswordChangeForm,
    SetPasswordForm,
    UserCreationForm,
)
from django.core.validators import FileExtensionValidator
from django.utils.translation import gettext_lazy as _


class SignupForm(UserCreationForm):
    """with password fields"""

    image = forms.ImageField(
        validators=[
            FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png", "gif"])
        ],
        required=False,
    )

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ("email", "username", "first_name", "last_name", "image")


class LoginForm(forms.Form):
    username = forms.CharField(label=_("Username"), required=True)
    password = forms.CharField(
        label=_("Password"), widget=forms.PasswordInput, required=True
    )

    def clean(self) -> dict:
        cleaned_data = super().clean()
        cleaned_username = cleaned_data.get("username")
        cleaned_password = cleaned_data.get("password")

        user = authenticate(username=cleaned_username, password=cleaned_password)
        if user is None:
            self.add_error("username", forms.ValidationError(""))
            self.add_error("password", forms.ValidationError(""))

            raise forms.ValidationError(_("Invalid credentials."))

        return cleaned_data


class AccountForm(forms.ModelForm):
    """without password fields"""

    image = forms.ImageField(
        validators=[
            FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png", "gif"]),
        ],
        required=False,
    )

    class Meta:
        model = get_user_model()
        fields = ("email", "username", "first_name", "last_name", "image")


class DeleteAccountForm(forms.Form):
    """to check csrf token"""

    pass


class ChangePasswordForm(PasswordChangeForm):
    pass


class ForgotPasswordForm(forms.Form):
    username = forms.CharField(label=_("Username"), required=True)
    email = forms.EmailField(required=True)

    def clean(self) -> dict:
        cleaned_data = super().clean()
        cleaned_username = cleaned_data.get("username")
        cleaned_email = cleaned_data.get("email")

        # check if username exists
        user = get_user_model().objects.filter(username=cleaned_username).first()
        if not user:
            self.add_error("username", forms.ValidationError(""))
            self.add_error("email", forms.ValidationError(""))

            raise forms.ValidationError(_("Invalid credentials."))

        # check if email is correct
        user.decrypt()
        if user.email != cleaned_email:
            self.add_error("username", forms.ValidationError(""))
            self.add_error("email", forms.ValidationError(""))

            raise forms.ValidationError(_("Invalid credentials."))

        return cleaned_data


class ResetPasswordForm(SetPasswordForm):
    pass

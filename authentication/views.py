from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views import View

from multilang_site.utils.jwt_token import Jwt

from .forms import (
    AccountForm,
    ChangePasswordForm,
    DeleteAccountForm,
    ForgotPasswordForm,
    LoginForm,
    ResetPasswordForm,
    SignupForm,
)


class Signup(View):
    def get(self, request):
        form = SignupForm()

        return render(request, "signup.html", {"form": form})

    def post(self, request):
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()

            messages.success(
                request, _("Account created successfully ! You are now able to login.")
            )

            return redirect("login")

        return render(request, "signup.html", {"form": form})


class Login(View):
    def get(self, request):
        form = LoginForm()

        return render(request, "login.html", {"form": form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            user = get_object_or_404(get_user_model(), username=username)
            user.decrypt()

            login(request, user)

            messages.success(request, _("Successfully logged in !"))

            next_page = request.GET.get("next")

            return redirect(next_page) if next_page else redirect("home")

        return render(request, "login.html", {"form": form})


class Logout(View):
    def get(self, request):
        logout(request)
        messages.info(request, _("You are now logged out."))

        return redirect("home")


class Account(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        user.decrypt()

        return render(request, "account.html", {"user": user})


class UpdateAccount(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        user.decrypt()

        form = AccountForm(instance=user)

        return render(request, "account_update.html", {"form": form})

    def post(self, request):
        user = request.user
        user.decrypt()

        form = AccountForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()

            messages.success(request, _("Account updated successfully !"))

            return redirect("account")

        return render(request, "account_update.html", {"form": form})


class DeleteAccount(LoginRequiredMixin, View):
    def post(self, request):
        form = DeleteAccountForm(request.POST)
        if form.is_valid():
            user = request.user
            logout(request)
            user.delete()
            messages.info(request, _("Your account has been deleted."))

            return redirect("home")


class ChangePassword(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        user.decrypt()
        form = ChangePasswordForm(user)

        return render(request, "password_update.html", {"form": form})

    def post(self, request):
        user = request.user
        user.decrypt()
        form = ChangePasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _("Password updated successfully !"))

            return redirect("login")

        return render(request, "password_update.html", {"form": form})


class ForgotPassword(View):
    def get(self, request):
        form = ForgotPasswordForm()

        return render(request, "password_forgot.html", {"form": form})

    def _generate_reset_password_url(self, request, username: str) -> str:
        token = Jwt.encode(payload_data={"username": username})

        if token:
            # reset password url
            internal_url = reverse("reset_password", kwargs={"token": token})
            external_url = request.build_absolute_uri(internal_url)

            return external_url

    def _html_message(self, username: str, reset_password_url: str) -> str:
        return """
        <html>
        <body>
            <p>{hello} {username},</p>
            <br><br>
            <p>{reset_info}</p>
            <p><a href="{reset_link}">{reset_button}</a></p>
            <p>{ignore_request}</p>
            <br><br>
            <p>{thank_you}</p>
            <p>Blogs Team</p>
        </body>
        </html>
        """.format(
            hello=_("Hello"),
            username=username,
            reset_info=_(
                "You are receiving this email because you requested a password reset for your account on our site."
            ),
            reset_link=reset_password_url,
            reset_button=_("Reset Your Password"),
            ignore_request=_(
                "If you did not request this reset, you can safely ignore this email. No changes will be made to your account."
            ),
            thank_you=_("Thank you,"),
        )

    def _send_email(self, username: str, email: str, reset_password_url: str) -> bool:
        """
        return True if the email  was sent
        return False the email was not sent
        """
        if not reset_password_url:
            return False

        try:
            send_mail(
                subject=_("Password Reset Request"),
                message="",
                from_email=f"No reply<{settings.EMAIL_HOST_USER}>",
                recipient_list=[email],
                html_message=self._html_message(username, reset_password_url),
            )

            return True

        except Exception as e:
            print(f"ForgotPassword.send_mail() error: {e}")

            return False

    def _show_message_flash(self, request, email_is_sent: bool):
        if email_is_sent:
            messages.info(
                request,
                _("Password reset email has been sent. Please check your inbox."),
            )
        else:
            messages.info(
                request,
                _("The service is currently unavailable. Please try again later."),
            )

    def post(self, request):
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            email = form.cleaned_data.get("email")

            reset_password_url = self._generate_reset_password_url(request, username)
            email_is_sent = self._send_email(username, email, reset_password_url)

            self._show_message_flash(request, email_is_sent)

            return redirect("home")

        return render(request, "password_forgot.html", {"form": form})


class ResetPassword(View):
    def _check_token(self, token):
        """raise 403 error if the token is not valid"""

        if not Jwt.verify(token):
            raise PermissionDenied

    def _get_user_from_token(self, token) -> get_user_model:
        self._check_token(token)
        username = Jwt.decode(token).get("username")
        user = get_object_or_404(get_user_model(), username=username)
        user.decrypt()

        return user

    def get(self, request, token):
        user = self._get_user_from_token(token)
        form = ResetPasswordForm(user)

        return render(request, "password_reset.html", {"form": form})

    def post(self, request, token):
        user = self._get_user_from_token(token)
        form = ResetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _("Password updated successfully !"))

            return redirect("login")

        return render(request, "password_reset.html", {"form": form})

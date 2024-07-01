from django.urls import path

from .views import (
    Account,
    ChangePassword,
    DeleteAccount,
    ForgotPassword,
    Login,
    Logout,
    ResetPassword,
    Signup,
    UpdateAccount,
)

urlpatterns = [
    path("signup/", Signup.as_view(), name="signup"),
    path("login/", Login.as_view(), name="login"),
    path("logout/", Logout.as_view(), name="logout"),
    path("account/", Account.as_view(), name="account"),
    path("account/update/", UpdateAccount.as_view(), name="update_account"),
    path("account/delete/", DeleteAccount.as_view(), name="delete_account"),
    path("account/password/change/", ChangePassword.as_view(), name="change_password"),
    path("account/password/forgot/", ForgotPassword.as_view(), name="forgot_password"),
    path(
        "account/<token>/password/reset/",
        ResetPassword.as_view(),
        name="reset_password",
    ),
]

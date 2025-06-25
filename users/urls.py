from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.views import (
    BlockUserView,
    CustomPasswordResetConfirmView,
    CustomPasswordResetView,
    ProfileDetailView,
    ProfileListView,
    ProfileUpdateView,
    RegisterView,
    email_verification,
)

app_name = UsersConfig.name

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(template_name="users/login.html"), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("email_confirm/<str:token>/", email_verification, name="email_confirm"),
    path("profile_edit/", ProfileUpdateView.as_view(), name="profile_edit"),
    path("profile/", ProfileDetailView.as_view(), name="profile"),
    path(
        "password_reset/",
        CustomPasswordResetView.as_view(template_name="users/password_reset_form.html"),
        name="password_reset",
    ),
    path(
        "password_reset_done/",
        auth_views.PasswordResetDoneView.as_view(template_name="users/password_reset_done.html"),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        CustomPasswordResetConfirmView.as_view(template_name="users/password_reset_confirm.html"),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(template_name="users/password_reset_complete.html"),
        name="password_reset_complete",
    ),
    path("user/<int:pk>/block/", BlockUserView.as_view(), name="block_user"),
    path("users/", ProfileListView.as_view(), name="profile_list"),
]

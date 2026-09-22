from django.contrib.auth import views
from django.contrib.auth.forms import AuthenticationForm

from .forms import LoginForm


class LoginView(views.LoginView):
    template_name: str | None = "accounts/login.html"
    next_page: str | None = "answers:index"
    authentication_form: type[AuthenticationForm] | None = LoginForm
    redirect_authenticated_user: bool = True


class LogoutView(views.LogoutView):
    next_page: str | None = "accounts:login"

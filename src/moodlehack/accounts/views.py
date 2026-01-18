from django.contrib.auth import views
from django.urls import reverse_lazy


class LoginView(views.LoginView):
    template_name = 'accounts/login.html'
    next_page = reverse_lazy('answers:index')
    redirect_authenticated_user = True


class LogoutView(views.LogoutView):
    next_page = reverse_lazy('accounts:login')

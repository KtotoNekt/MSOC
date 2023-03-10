from django.contrib.auth import logout, authenticate, login, get_user_model
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView
from django.core.exceptions import ValidationError
from django.http import Http404
from django.shortcuts import redirect, render
from django.utils.http import urlsafe_base64_decode
from django.views import View
from django.contrib.auth.tokens import default_token_generator as token_generator

from .forms import RegisterUserForm, LoginUserForm, CustomPasswordResetForm, CustomSetPasswordForm
from django.views.generic import CreateView

from .utils import send_email_for_verify


User = get_user_model()

# Create your views here.
def logout_user(req):
    logout(req)
    return redirect('login')


class RegisterView(CreateView):
    template_name = "users/register.html"
    model = User
    form_class = RegisterUserForm

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password1")
            user = authenticate(email=email, password=password)
            send_email_for_verify(request, user)
            return redirect('confirm_email')

        context = {
            'form': form
        }
        return render(request, self.template_name, context)


class EmailVerify(View):
    def get(self, request, uidb64, token):
        user = self.get_user(uidb64)

        if user is not None and token_generator.check_token(user, token):
            user.email_verify = True
            user.save()
            login(request, user)
            return redirect('main')

        raise Http404()

    @staticmethod
    def get_user(uidb64):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError,
                User.DoesNotExist, ValidationError):
            user = None
        return user


class CustomLoginView(LoginView):
    form_class = LoginUserForm
    template_name = "users/login.html"
    success_url = "/"


class CustomPasswordReset(PasswordResetView):
    template_name = "users/password_reset_form.html"
    form_class = CustomPasswordResetForm
    success_url = "/users/password_reset/done"
    email_template_name = "users/password_reset_email.html"


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = "users/password_reset_done.html"


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "users/password_reset_confirm.html"
    form_class = CustomSetPasswordForm
    success_url = "/users/login"

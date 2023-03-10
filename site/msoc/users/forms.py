from django.contrib.auth import get_user_model, authenticate
from django.core.exceptions import ValidationError
from django.forms import TextInput, EmailField, EmailInput, PasswordInput, CharField
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm

from .utils import send_email_for_verify

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User


class RegisterUserForm(CustomUserCreationForm):
    email = EmailField(widget=EmailInput(attrs={
                "class": "form-control",
                "placeholder": "Email (по нему вы будите входить в систему)"
            }))
    password1 = CharField(widget=PasswordInput(attrs={
                "class": "form-control",
                "placeholder": "Пароль",
                "autocomplete": "new-password"
            }))
    password2 = CharField(widget=PasswordInput(attrs={
                "class": "form-control",
                "placeholder": "Подтверждение пароля",
                "autocomplete": "new-password"
            }))

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2",)

        widgets = {
            "username": TextInput(attrs={
                "class": "form-control",
                "placeholder": "Имя пользователя"
            }),
        }


class LoginUserForm(AuthenticationForm):
    username = CharField(label='Логин', widget=TextInput(attrs={
        'class': 'form-control',
        "placeholder": "Email"
    }))
    password = CharField(label='Пароль', widget=PasswordInput(attrs={
        'class': 'form-control',
        "placeholder": "Пароль"
    }))

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username is not None and password:
            self.user_cache = authenticate(
                self.request,
                username=username,
                password=password,
            )

            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise ValidationError(
                self.error_messages["inactive"],
                code="inactive",
            )
        elif not user.email_verify:
            send_email_for_verify(self.request, self.user_cache)
            raise ValidationError(
                'Вы не подтвердили свою почту. Мы повторно отправили вам письмо с подтверждением!',
                code='invalid_login',
            )


class CustomPasswordResetForm(PasswordResetForm):
    email = EmailField(widget=EmailInput(attrs={
        'class': 'form-control',
        "placeholder": "Email учетной записи"
    }))


class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = CharField(strip=False, widget=PasswordInput(attrs={
        "class": "form-control",
        "placeholder": "Новый пароль",
        "autocomplete": "new-password"
    }))
    new_password2 = CharField(strip=False, widget=PasswordInput(attrs={
        "class": "form-control",
        "placeholder": "Подтверждение нового пароля",
        "autocomplete": "new-password"
    }))


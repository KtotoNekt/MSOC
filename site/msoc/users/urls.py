from django.urls import path, include
from django.views.generic import TemplateView

from django.conf import settings
from django.conf.urls.static import static

from .views import *


urlpatterns = [
    path("confirm_email/", TemplateView.as_view(template_name="users/confirm_email.html"), name="confirm_email"),
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", logout_user, name="logout"),
    path("password_reset/", CustomPasswordReset.as_view(), name="password_reset"),
    path("password_reset/done/", CustomPasswordResetDoneView.as_view(), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", CustomPasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path(
        'verify_email/<uidb64>/<token>/',
        EmailVerify.as_view(),
        name='verify_email',
    ),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
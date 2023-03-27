from django.urls import path
from .views import *

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", complaints_view, name='complaints'),
    path("delete/<int:complaint_id>", delete_complaint, name='delete_complaint'),
    path("create/<int:music_id>", CreateComplaintView.as_view(), name='create_complaint'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

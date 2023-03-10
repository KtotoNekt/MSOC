from django.urls import path
from .views import *

urlpatterns = [
    path("", complaints_view, name='complaints'),
    path("delete/<int:complaint_id>", delete_complaint, name='delete_complaint'),
    path("create/<int:music_id>", CreateComplaintView.as_view(), name='create_complaint'),
]

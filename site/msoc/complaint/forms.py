from django.forms import ModelForm, TextInput, Textarea, Select, CharField

from .models import Complaint


class ComplaintForm(ModelForm):
    class Meta:
        model = Complaint
        fields = ["reason", "description"]

        widgets = {
            "reason": Select(choices=Complaint.REASONS, attrs={
                "class": "form-control",
            }),
            "description": Textarea(attrs={
                "class": "form-control",
                "placeholder": "Описание проблемы"
            })
        }


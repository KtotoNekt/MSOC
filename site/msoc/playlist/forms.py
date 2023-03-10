from .models import PlayList
from django.forms import ModelForm, TextInput


class PlayListForm(ModelForm):
    class Meta:
        model = PlayList
        fields = ["name", "description"]

        widgets = {
            "name": TextInput(attrs={
                "class": "form-control",
                "placeholder": "Название плейлиста"
            }),
            "description": TextInput(attrs={
                "class": "form-control",
                "placeholder": "Описание плейлиста"
            }),
        }

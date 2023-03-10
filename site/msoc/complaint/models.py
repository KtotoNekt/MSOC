from django.contrib.auth import get_user_model
from django.db import models

from main.models import Music

User = get_user_model()

# Create your models here.
class Complaint(models.Model):
    REASONS = [
        ("Неполный трек", "Неполный трек"),
        ("Не является треком", "Не является треком"),
        ("Другое", "Другое")
    ]

    reason = models.CharField(max_length=20,  choices=REASONS, blank=False, default=2)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    music = models.ForeignKey(Music, on_delete=models.CASCADE)


# from complaint.models import Complaint

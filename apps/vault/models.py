from django.db import models
from apps.challenges.models import Gadget

class Submission(models.Model):
    gadget = models.ForeignKey(Gadget, on_delete=models.CASCADE, related_name='submissions')
    file_path = models.CharField(max_length=500)  # Csak az útvonalat tároljuk
    status = models.CharField(max_length=20, default='pending')
    uploaded_at = models.DateTimeField(auto_now_add=True)
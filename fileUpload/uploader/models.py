from django.db import models
from .utils.utils import upload_path,validate_file_size

class Upload(models.Model):
    file = models.FileField(upload_to=upload_path,validators=[validate_file_size])
    uploaded_at = models.DateTimeField(auto_now_add=True)
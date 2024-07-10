from django.db import models
from .utils.utils import upload_path,validate_file_size
from django.contrib.auth.models import User

class Upload(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    file = models.FileField(upload_to=upload_path,validators=[validate_file_size])
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False) 

    def __str__(self):
        return self.file.name
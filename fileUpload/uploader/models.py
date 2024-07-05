from django.db import models
import os
from datetime import datetime

from django.forms import ValidationError
# Create your models here.


def upload_path(instance, file):
    
   file_extension = os.path.splitext(file)[1].lower()
   if file_extension in ['.jpg', '.jpeg', '.png', '.gif']:
        folder_name = 'pictures'
   elif file_extension in ['.mp4', '.avi', '.mov']:
        folder_name = 'video'
   else:
        raise ValueError('Unsupported file format')
   
   today = datetime.now()
   year = str(today.year)
   month = str(today.month)
   day = str(today.day)

   return os.path.join(f"uploads/{year}/{month}/{day}/{folder_name}", file)

def validate_file_size(value):
    limit_mb = 20
    if value.size > limit_mb * 1024 * 1024:
        raise ValidationError(f"File size exceeds {limit_mb} MB.")

class Upload(models.Model):
    file = models.FileField(upload_to=upload_path,validators=[validate_file_size])
    uploaded_at = models.DateTimeField(auto_now_add=True)
# Generated by Django 4.2.13 on 2024-07-09 13:07

from django.db import migrations, models
import uploader.utils.utils


class Migration(migrations.Migration):

    dependencies = [
        ('uploader', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='upload',
            name='file',
            field=models.FileField(upload_to=uploader.utils.utils.upload_path, validators=[uploader.utils.utils.validate_file_size]),
        ),
    ]

import os
import uuid

from django.db import models
from django.core.validators import FileExtensionValidator


def get_upload_path(instance, filename):
    name, ext = os.path.splitext(filename)
    return os.path.join('images', f'{instance.id}{ext}')


class Images(models.Model):
    validate_file = FileExtensionValidator(allowed_extensions=['jpeg', 'png',])

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file = models.FileField(upload_to=get_upload_path,
                            validators=[validate_file])
    location = models.CharField(max_length=128, db_index=True)
    description = models.TextField()
    date = models.DateTimeField()
    people = models.ManyToManyField('images.Person')


class Person(models.Model):
    name = models.CharField(max_length=32, db_index=True)

# Generated by Django 3.1 on 2022-12-18 18:52

import django.core.validators
from django.db import migrations, models
import images.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('file', models.FileField(upload_to=images.models.get_upload_path, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['image/jpeg', 'image/png'])])),
                ('location', models.CharField(db_index=True, max_length=128)),
                ('description', models.TextField()),
                ('date', models.DateTimeField()),
                ('people', models.ManyToManyField(to='images.Person')),
            ],
        ),
    ]

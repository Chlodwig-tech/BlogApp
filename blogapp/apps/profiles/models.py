from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
import uuid

def validate_file_size(value):
    image_size = value.size
    if image_size > 1024 * 256:
        raise ValidationError('File size cannot exceed 0.5 MB.')

def generate_unique_filename(_, filename):
    ext = filename.split('.')[-1]
    unique_filename = f'{uuid.uuid4()}.{ext}'
    return f'profile_images/{unique_filename}'
    

# Create your models here.
class Profile(models.Model):
    user  = models.ForeignKey(User, on_delete=models.CASCADE)
    bio   = models.CharField(max_length=240, blank=True)
    image = models.ImageField(
        upload_to=generate_unique_filename,
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png']),
            validate_file_size
        ],
        blank=True,
        null=True
    )

    def __str__(self):
        return f'{self.user}'
    
    def img_src(self):
        return f'/media/{self.image}' if self.image else "/static/favicons/favicon.ico"
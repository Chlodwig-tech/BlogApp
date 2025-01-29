from django.db import models
from django.conf import settings
from datetime import datetime, timezone
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth.models import User
from unidecode import unidecode
from django_ckeditor_5.fields import CKEditor5Field
from random import randint

from apps.profiles.models import Profile
from apps.comments.models import Comment
    
class Post(models.Model):
    class Meta:
        ordering = ["-publish_date"]

    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255, blank=True)
    slug = models.SlugField(max_length=255, unique=True)
    body = CKEditor5Field()
    meta_description = models.CharField(max_length=150, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    publish_date = models.DateTimeField(blank=True, null=True)
    published = models.BooleanField(default=False)

    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    root_comment = models.ForeignKey(Comment, on_delete=models.CASCADE, blank=True, null=True)

    def get_post_preview(self):
        return self.body[:200] + '...'

    def number_of_views(self):
        return len(self.body)

    def time_passed_from_date(self):
        current_date = datetime.now(timezone.utc)
        time_difference = current_date - self.publish_date

        days = time_difference.days
        if days > 365:
            return f'{int(days / 365)} lat temu'

        if days > 0:
            return f'{days} dni temu'
        
        seconds = time_difference.seconds
        if seconds > 3600:
            return f'{int(seconds / 3600)} godzin temu'

        if seconds > 60:
           return f'{int(seconds / 60)} minut temu' 

        return f'{seconds} sekund temu'

    def get_published_date(self):
        import locale
        locale.setlocale(locale.LC_TIME, 'pl_PL.utf8')
        input_format = '%d %B %Y'
        return self.publish_date.date().strftime(input_format)

    def get_published_hour(self):
        minutes = self.publish_date.minute
        minutes = f'{minutes}' if minutes > 9 else f'0{minutes}'
        return f'{self.publish_date.hour}:{minutes}'
    
    def get_slug(self):
        return f'{slugify(unidecode(self.title))}-{randint(1,10000)}'
    
    def get_absolute_url(self):
        return reverse('posts-detail', kwargs={'slug':self.slug})
    def get_absolute_delete_url(self):
        return reverse('posts-delete', kwargs={'slug':self.slug})
    def get_absolute_edit_url(self):
        return reverse('posts-edit', kwargs={'slug':self.slug})
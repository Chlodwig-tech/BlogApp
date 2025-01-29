from django.db import models
from datetime import datetime, timezone

from apps.profiles.models import Profile

class Comment(models.Model):
    author            = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, null=True)
    children_comments = models.ManyToManyField('self', blank=True, symmetrical=False)
    publish_date      = models.DateTimeField(blank=True, null=True)
    content           = models.CharField(max_length=150, blank=True)

    def time_passed_from_date(self):
        return self.publish_date.strftime('%d.%m.%Y' if (datetime.now(timezone.utc) - self.publish_date).days > 0 else '%H:%M')
    
    def delete_comment(self):
        for child in self.children_comments.all():
            child.delete_comment()
        self.delete()
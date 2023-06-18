from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User


class Musicdata(models.Model):
    VISIBILITY_CHOICES = [
        ('public', 'Public'),
        ('private', 'Private'),
        ('protected', 'Protected'),
    ]

    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='musicdata/')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    visibility = models.CharField(max_length=10, choices=VISIBILITY_CHOICES)
    allowed_emails = models.TextField(blank=True, null=True)
    access_emails = models.TextField(blank=True, null=True)

    def has_access(self, email):
        if self.visibility == 'public':
            return True
        elif self.visibility == 'private':
            return self.user.email == email
        elif self.visibility == 'protected':
            return email in self.access_emails.split(',') if self.access_emails else False
        return False


def __str__(self):
    return self.title

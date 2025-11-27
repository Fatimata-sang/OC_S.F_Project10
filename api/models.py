from django.db import models

from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """ Custom User model for creating users"""

    # added age verification and consents fields for legal and GDPR requirements.
    age = models.IntegerField(verbose_name="age")
    contact_consent = models.BooleanField(default=False, verbose_name="contact consent")
    data_share_consent = models.BooleanField(default=False, verbose_name="data share consent")

    def __str__(self):
        return self.username


class Project(models.Model):
    """ Project model for creating projects"""

    objects = None

    # Short project_types
    BACKEND = "B"
    FRONTEND = "F"
    IOS = "I"
    ANDROID = "A"

    # Long project_types
    PROJECT_TYPES = [
        (BACKEND, "Back-end"),
        (FRONTEND, "Front-end"),
        (IOS, "iOS"),
        (ANDROID, "Android"),
    ]

    name = models.CharField(max_length=100, verbose_name="name of project")
    description = models.TextField(verbose_name="project description")
    type = models.CharField(max_length=1, choices=PROJECT_TYPES, verbose_name="project type")
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        related_name="project_author",
        verbose_name="project author",
    )
    contributors = models.ManyToManyField(
        User,
        blank=True,
        related_name="project_contributors",
        verbose_name="project contributors",
    )

    created_time = models.DateTimeField(auto_now_add=True, verbose_name="created on")
    updated_time = models.DateTimeField(auto_now=True, verbose_name="updated on")

    def __str__(self):
        return f"Project: {self.name} ¦ Author: {self.author}"


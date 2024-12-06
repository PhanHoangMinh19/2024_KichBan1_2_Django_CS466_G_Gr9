from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    access_level = models.CharField(max_length=50, choices=[('user', 'User'), ('content manager', 'Content Manager'), ('admin', 'Admin')], default='user')

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='library_user_set',  # Add this related_name to avoid clashes
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='library_user_set',  # Add this related_name to avoid clashes
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def __str__(self):
        return self.username

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        CITIZEN = "CITIZEN", "Citizen"
        POLICE = "POLICE", "Police Officer"
        ADMIN = "ADMIN", "Admin"

    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.CITIZEN,
    )

    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def is_citizen(self):
        return self.role == self.Role.CITIZEN

    def is_police(self):
        return self.role == self.Role.POLICE

    def __str__(self):
        return f"{self.username} ({self.role})"
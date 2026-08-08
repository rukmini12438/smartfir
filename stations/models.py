from django.db import models
from django.conf import settings


class PoliceStation(models.Model):
    name = models.CharField(max_length=200)
    jurisdiction_area = models.CharField(max_length=200)
    address = models.TextField()
    contact_number = models.CharField(max_length=15)

    def __str__(self):
        return self.name


class PoliceOfficerProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="police_profile",
    )

    station = models.ForeignKey(
        PoliceStation,
        on_delete=models.SET_NULL,
        null=True,
        related_name="officers",
    )

    badge_number = models.CharField(max_length=20, unique=True)
    rank = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({self.badge_number})"
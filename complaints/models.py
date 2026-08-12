from django.db import models
from django.conf import settings
from stations.models import PoliceStation


class Complaint(models.Model):
    class Status(models.TextChoices):
        SUBMITTED = "SUBMITTED", "Submitted"
        UNDER_REVIEW = "UNDER_REVIEW", "Under Review"
        CONVERTED = "CONVERTED", "Converted to FIR"
        REJECTED = "REJECTED", "Rejected"

    class Urgency(models.TextChoices):
        HIGH = "HIGH", "High"
        MEDIUM = "MEDIUM", "Medium"
        LOW = "LOW", "Low"

    citizen = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="complaints",
    )

    description = models.TextField()
    location = models.CharField(max_length=255)
    incident_date = models.DateField(null=True, blank=True)

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.SUBMITTED,
    )

    embedding = models.JSONField(null=True, blank=True)

    urgency = models.CharField(
        max_length=10,
        choices=Urgency.choices,
        null=True,
        blank=True,
    )
    # AI complaint padh ke decide karega ye kitna urgent hai —
    # taaki police dashboard mein sabse pehle sabse zaroori
    # cases dikhein, sabse purani complaint nahi

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Complaint #{self.id} by {self.citizen.username}"


class FIR(models.Model):
    class Status(models.TextChoices):
        REGISTERED = "REGISTERED", "Registered"
        INVESTIGATION = "INVESTIGATION", "Under Investigation"
        CLOSED = "CLOSED", "Closed"

    complaint = models.OneToOneField(
        Complaint,
        on_delete=models.CASCADE,
        related_name="fir",
    )

    fir_number = models.CharField(max_length=50, unique=True)

    station = models.ForeignKey(
        PoliceStation,
        on_delete=models.SET_NULL,
        null=True,
        related_name="firs",
    )

    formal_description = models.TextField(blank=True)
    suggested_sections = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.REGISTERED,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.fir_number
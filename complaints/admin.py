from django.contrib import admin
from .models import Complaint, FIR

admin.site.register(Complaint)
admin.site.register(FIR)
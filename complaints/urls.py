from django.urls import path
from .views import (
    ComplaintListCreateView,
    ComplaintDetailView,
    SimilarComplaintsView,
    FIRListCreateView,
    FIRDetailView,
)

urlpatterns = [
    path("", ComplaintListCreateView.as_view(), name="complaint-list-create"),
    path("<int:pk>/", ComplaintDetailView.as_view(), name="complaint-detail"),
    path("<int:pk>/similar/", SimilarComplaintsView.as_view(), name="complaint-similar"),
    path("firs/", FIRListCreateView.as_view(), name="fir-list-create"),
    path("firs/<int:pk>/", FIRDetailView.as_view(), name="fir-detail"),
]
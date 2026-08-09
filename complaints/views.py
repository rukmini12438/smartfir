from rest_framework import generics, permissions
from .models import Complaint, FIR
from .serializers import ComplaintSerializer, FIRSerializer


class ComplaintListCreateView(generics.ListCreateAPIView):
    """
    Ek hi View se 2 kaam ho rahe hain (DRF ka pattern hai):
    - GET request -> saari complaints ki LIST dikhao
    - POST request -> nayi complaint CREATE karo
    """
    serializer_class = ComplaintSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Role ke hisaab se alag data dikhana:
        user = self.request.user
        if user.is_police():
            # Police ko SAARI complaints dikhni chahiye (sabhi citizens ki)
            return Complaint.objects.all().order_by("-created_at")
        # Citizen ko SIRF apni khud ki complaints dikhni chahiye
        return Complaint.objects.filter(citizen=user).order_by("-created_at")

    def perform_create(self, serializer):
        # Jab naya complaint create ho, 'citizen' field automatically
        # current logged-in user se fill ho jaye (user ko khud se
        # bhejne ki zaroorat nahi, aur security ke liye bhi behtar hai)
        serializer.save(citizen=self.request.user)


class ComplaintDetailView(generics.RetrieveUpdateAPIView):
    """
    Ek SPECIFIC complaint ki detail dikhana (GET) ya update karna (PUT/PATCH).
    URL mein complaint ka ID aayega, jaise /api/complaints/5/
    """
    serializer_class = ComplaintSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Complaint.objects.all()


class FIRListCreateView(generics.ListCreateAPIView):
    """
    FIR list dekhna aur naya FIR banana — abhi ke liye ye sirf
    Police access karega (citizens FIR khud nahi bana sakte,
    wo sirf complaint file karte hain).
    """
    serializer_class = FIRSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_police():
            return FIR.objects.all().order_by("-created_at")
        # Citizen sirf apni complaints se bane FIRs dekh sakta hai
        return FIR.objects.filter(complaint__citizen=user).order_by("-created_at")


class FIRDetailView(generics.RetrieveUpdateAPIView):
    """
    Ek specific FIR ki detail dekhna ya update karna
    (jaise Police status change kare "Under Investigation" se "Closed")
    """
    serializer_class = FIRSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = FIR.objects.all()
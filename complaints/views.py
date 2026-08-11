from rest_framework import generics, permissions
from .models import Complaint, FIR
from .serializers import ComplaintSerializer, FIRSerializer
from .ai_service import generate_fir_draft


class ComplaintListCreateView(generics.ListCreateAPIView):
    serializer_class = ComplaintSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_police():
            return Complaint.objects.all().order_by("-created_at")
        return Complaint.objects.filter(citizen=user).order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(citizen=self.request.user)


class ComplaintDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = ComplaintSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Complaint.objects.all()


class FIRListCreateView(generics.ListCreateAPIView):
    serializer_class = FIRSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_police():
            return FIR.objects.all().order_by("-created_at")
        return FIR.objects.filter(complaint__citizen=user).order_by("-created_at")

    def perform_create(self, serializer):
        # Complaint object nikalte hain jiska FIR bana rahe hain
        complaint = serializer.validated_data["complaint"]

        # AI se formal FIR draft aur legal sections generate karwate hain
        ai_result = generate_fir_draft(
            complaint_description=complaint.description,
            location=complaint.location,
        )

        # AI ke result ko FIR object mein save karte hain
        serializer.save(
            formal_description=ai_result["formal_description"],
            suggested_sections=ai_result["suggested_sections"],
        )


class FIRDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = FIRSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = FIR.objects.all()
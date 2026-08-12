from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from .models import Complaint, FIR
from .serializers import ComplaintSerializer, FIRSerializer
from .pattern_service import get_embedding, find_similar_complaints
from .ai_service import generate_fir_draft, transcribe_audio, classify_urgency

class ComplaintListCreateView(generics.ListCreateAPIView):
    serializer_class = ComplaintSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_police():
            return Complaint.objects.all().order_by("-created_at")
        return Complaint.objects.filter(citizen=user).order_by("-created_at")

    def perform_create(self, serializer):
        complaint = serializer.save(citizen=self.request.user)
        try:
            complaint.embedding = get_embedding(complaint.description)
            complaint.urgency = classify_urgency(complaint.description)
            complaint.save()
        except Exception as e:
            print(f"Post-processing failed: {e}")


class ComplaintDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = ComplaintSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Complaint.objects.all()


class SimilarComplaintsView(APIView):
    """
    Police ke liye — ek complaint ke liye 'kya iske jaisi aur bhi
    complaints hain' check karta hai (pattern detection).
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        try:
            target = Complaint.objects.get(pk=pk)
        except Complaint.DoesNotExist:
            return Response({"error": "Complaint not found"}, status=404)

        all_complaints = Complaint.objects.exclude(pk=pk)
        similar = find_similar_complaints(target, all_complaints)

        results = [
            {
                "id": item["complaint"].id,
                "description": item["complaint"].description,
                "location": item["complaint"].location,
                "citizen_username": item["complaint"].citizen.username,
                "similarity_score": item["similarity_score"],
            }
            for item in similar
        ]
        return Response(results)


class FIRListCreateView(generics.ListCreateAPIView):
    serializer_class = FIRSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_police():
            return FIR.objects.all().order_by("-created_at")
        return FIR.objects.filter(complaint__citizen=user).order_by("-created_at")

    def perform_create(self, serializer):
        complaint = serializer.validated_data["complaint"]
        ai_result = generate_fir_draft(
            complaint_description=complaint.description,
            location=complaint.location,
        )
        serializer.save(
            formal_description=ai_result["formal_description"],
            suggested_sections=ai_result["suggested_sections"],
        )


class TranscribeAudioView(APIView):
    """
    Audio recording accept karta hai (browser se), Gemini se
    transcribe karwata hai, aur text wapas bhejta hai.
    """
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser]
    # MultiPartParser zaroori hai kyunki humein file upload
    # (audio) accept karni hai, sirf JSON nahi

    def post(self, request):
        audio_file = request.FILES.get("audio")
        if not audio_file:
            return Response({"error": "No audio file provided"}, status=400)

        try:
            text = transcribe_audio(
                audio_file.read(),
                audio_file.content_type or "audio/webm",
            )
            return Response({"text": text})
        except Exception as e:
            print(f"Transcription failed: {e}")
            return Response({"error": "Transcription failed"}, status=500)        


class FIRDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = FIRSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = FIR.objects.all()


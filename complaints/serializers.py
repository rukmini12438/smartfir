from rest_framework import serializers
from .models import Complaint, FIR


class ComplaintSerializer(serializers.ModelSerializer):
    """
    Complaint create karne aur list/detail dikhane, dono ke liye
    use hoga. 'citizen' field ko read_only rakha hai kyunki wo
    hum khud view mein set karenge (jo bhi logged-in user hai,
    wahi citizen hoga) — user ko khud se citizen ID bhejne dena
    security risk hota (koi aur ke naam se complaint file kar sakta).
    """

    citizen_username = serializers.CharField(source="citizen.username", read_only=True)
    # source="citizen.username" — ye related User model ke andar jaake
    # uska username nikal ke ek naya readable field bana deta hai response mein,
    # taaki frontend ko citizen ka naam dikhane ke liye alag API call na karni pade

    class Meta:
        model = Complaint
        fields = [
            "id",
            "citizen",
            "citizen_username",
            "description",
            "location",
            "incident_date",
            "status",
            "created_at",
        ]
        read_only_fields = ["citizen", "status", "created_at"]
        # citizen -> humne khud set karna hai (upar wajah bataya)
        # status -> naya complaint hamesha "SUBMITTED" se shuru hoga, user khud status set nahi kar sakta
        # created_at -> automatically system set karta hai


class FIRSerializer(serializers.ModelSerializer):
    """
    FIR dikhane/create karne ke liye. Abhi ke liye simple rakha hai —
    Phase 1-3 mein jab AI integrate hoga, formal_description aur
    suggested_sections fields AI se automatically fill hone lagenge.
    """

    complaint_description = serializers.CharField(source="complaint.description", read_only=True)

    class Meta:
        model = FIR
        fields = [
            "id",
            "complaint",
            "complaint_description",
            "fir_number",
            "station",
            "formal_description",
            "suggested_sections",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]
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
            "urgency",
            "created_at",
        ]
        read_only_fields = ["citizen", "status", "urgency", "created_at"]
        # citizen -> humne khud set karna hai
        # status -> naya complaint hamesha "SUBMITTED" se shuru hoga
        # urgency -> AI automatically set karega, user nahi
        # created_at -> automatically system set karta hai


class FIRSerializer(serializers.ModelSerializer):
    """
    FIR dikhane/create karne ke liye.
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
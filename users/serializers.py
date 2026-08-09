from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer ka kaam hai Django model object (Python object) ko
    JSON mein convert karna (aur JSON se wapas Python object mein) —
    taaki React frontend isse samajh sake, aur data validate ho sake.
    """

    class Meta:
        model = User
        fields = ["id", "username", "email", "role", "phone_number"]
        # Sirf ye fields JSON response mein bhejenge — password kabhi
        # response mein nahi jayega (security ke liye)


class RegisterSerializer(serializers.ModelSerializer):
    """
    Sirf REGISTER (naya account banane) ke liye alag serializer —
    isme password bhi include hota hai (input ke liye), jo
    UserSerializer mein nahi hai (output ke liye).
    """

    password = serializers.CharField(write_only=True, min_length=6)
    # write_only=True = ye field sirf INPUT (jab user data bhejta hai) mein
    # accept hoga, lekin OUTPUT (response) mein kabhi wapas nahi bheja jayega

    class Meta:
        model = User
        fields = ["username", "email", "password", "role", "phone_number"]

    def create(self, validated_data):
        # Django ka default create() password ko PLAIN TEXT mein save
        # kar deta, jo bahut unsafe hai. Isliye hum khud override kar rahe
        # hain taaki password hash (encrypt) hoke save ho.
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email", ""),
            password=validated_data["password"],
            role=validated_data.get("role", User.Role.CITIZEN),
            phone_number=validated_data.get("phone_number", ""),
        )
        return user
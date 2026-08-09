from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User
from .serializers import UserSerializer, RegisterSerializer


class RegisterView(generics.CreateAPIView):
    """
    generics.CreateAPIView Django REST Framework ka ek ready-made
    class hai jo POST request handle karta hai — hume sirf batana
    hai kaunsa serializer aur kaunsa data (queryset) use karna hai,
    baaki logic (validate, save, response bhejna) ye khud handle karta hai.
    """
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
    # AllowAny = koi bhi (bina login kiye) is API ko call kar sakta hai
    # (obviously — register karne ke liye login ki zaroorat nahi hoti)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Login karte waqt hum sirf token nahi, user ka role bhi
    frontend ko bhejna chahte hain (taaki React turant decide kar sake
    Citizen dashboard dikhana hai ya Police dashboard).
    Isliye default JWT serializer ko thoda customize kar rahe hain.
    """

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["role"] = user.role
        token["username"] = user.username
        return token


class LoginView(TokenObtainPairView):
    # TokenObtainPairView already pura login logic handle karta hai
    # (username-password check karna, JWT access+refresh token banana)
    # Hume bas apna custom serializer point karna hai
    serializer_class = CustomTokenObtainPairSerializer


class LogoutView(APIView):
    """
    JWT mein "logout" ka concept thoda alag hota hai session-based auth se.
    Yahan hum user ka refresh token "blacklist" (permanently invalid) kar
    dete hain, taaki wo dobara naya access token generate na kar sake.
    """
    permission_classes = [permissions.IsAuthenticated]
    # IsAuthenticated = sirf logged-in user hi ye API call kar sakta hai

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class GetMeView(APIView):
    """
    Frontend ko batata hai "abhi kaun logged in hai" — page reload
    hone par bhi React ko pata chal sake ki current user kaun hai,
    uska role kya hai, waghera.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
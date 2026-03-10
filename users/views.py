from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import User
from .serializers import UserSerializer


class UserCreateView(generics.CreateAPIView):
    """
    Vue dédiée à la création d’utilisateur (inscription), accessible sans authentification.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class UserViewSet(viewsets.ModelViewSet):
    """
    Vue pour opérations CRUD sur utilisateurs existants, accessible uniquement aux utilisateurs authentifiés.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
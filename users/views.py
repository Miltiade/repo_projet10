from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated, AllowAny, BasePermission
from .models import User
from .serializers import UserSerializer

class IsOwner(BasePermission):
    """
    Permission qui permet l’accès uniquement à l’objet appartenant à l’utilisateur connecté.
    """
    def has_object_permission(self, request, view, obj):
        return obj == request.user

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
    serializer_class = UserSerializer # Identifie le projet lié à l'objet
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        # L’utilisateur ne reçoit en réponse que ses propres données
        return User.objects.filter(pk=self.request.user.pk)
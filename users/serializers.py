from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # Liste des champs à exposer / manipuler via l’API
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'role', 'can_be_contacted', 'can_data_be_shared', 'date_of_birth',
        ]
        # On peut en exclure certains via `exclude` si besoin
        # Exclure le mot de passe et autres champs sensibles
from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # Liste des champs à exposer / manipuler via l’API
        fields = [
            'id', 'username', 'role', 'can_be_contacted', 'can_data_be_shared', 'date_of_birth',
        ]
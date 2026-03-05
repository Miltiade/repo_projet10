from rest_framework import serializers
from .models import User
from django.utils import timezone

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # Liste des champs à exposer / manipuler via l’API
        fields = [
            'id', 'username', 'role', 'can_be_contacted', 'can_data_be_shared', 'date_of_birth',
        ]

    def validate_date_of_birth(self, value):
        if value is None:
            raise serializers.ValidationError("Renseigner la date de naissance est obligatoire.")
        today = timezone.now().date()
        age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
        if age < 15:
            raise serializers.ValidationError("Inscription interdite : l'utilisateur doit avoir au moins 15 ans pour créer un compte.")
        return value
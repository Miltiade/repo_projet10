from rest_framework import serializers
from .models import User
from django.utils import timezone

class UserSerializer(serializers.ModelSerializer):
    can_be_contacted = serializers.BooleanField(
        required=True,
        error_messages={'required': 'Consentez-vous à être contacté ? Réponse obligatoire.'}
    )
    can_data_be_shared = serializers.BooleanField(
        required=True,
        error_messages={'required': 'Consentez-vous au partage de vos données ? Réponse obligatoire.'}
    )
    date_of_birth = serializers.DateField(
        required=True,
        error_messages={'required': 'Renseigner la date de naissance est obligatoire.'}
    )

    class Meta:
        model = User
        fields = [
            'id', 'username', 'role', 'can_be_contacted', 'can_data_be_shared', 'date_of_birth',
        ]

    def validate_date_of_birth(self, value):
        today = timezone.now().date()
        age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
        if age < 15:
            raise serializers.ValidationError("Inscription interdite : l'utilisateur doit avoir au moins 15 ans pour créer un compte.")
        return value
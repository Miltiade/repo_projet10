from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    ROLE_CHOICES = (
        ('author', 'Author'),
        ('contributor', 'Contributor'),
        ('user', 'User'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')

    def is_author(self):
        return self.role == 'author'

    def is_contributor(self):
        return self.role == 'contributor'

    def is_admin(self):
        return self.role == 'admin'
    
    can_be_contacted = models.BooleanField(default=True)

    can_data_be_shared = models.BooleanField(default=False)

    date_of_birth = models.DateField(null=True, blank=True)

    def is_of_age(self, age_limit=15):
        if not self.date_of_birth:
            return False
        today = timezone.now().date()
        age = today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )
        return age >= age_limit
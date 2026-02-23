from django.db import models
from users.models import User  # Import de votre modèle User personnalisé

class Project(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Contributor(models.Model):
    ROLE_CHOICES = (
        ('author', 'Author'),
        ('contributor', 'Contributor'),
    )

    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='contributions')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='contributors')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    date_joined = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'project')  # un utilisateur ne peut contribuer qu’une fois par projet

    def __str__(self):
        return f"{self.user.username} - {self.project.title} ({self.role})"
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Project, Contributor, Issue, Comment
from .serializers import ProjectSerializer, ContributorSerializer, IssueSerializer, CommentSerializer
from .permissions import IsProjectContributor, IsAuthorOrReadOnly, IsContributorCreatePermission


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsProjectContributor, IsAuthorOrReadOnly, IsContributorCreatePermission]

    def perform_create(self, serializer):
        # Lors de la création, l'utilisateur devient auteur et contributeur
        project = serializer.save(author=self.request.user)
        Contributor.objects.create(
            user=self.request.user,
            project=project,
            role='author'
        )

class ContributorViewSet(viewsets.ModelViewSet):
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

class IssueViewSet(viewsets.ModelViewSet):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated, IsProjectContributor, IsAuthorOrReadOnly, IsContributorCreatePermission]

    def perform_create(self, serializer):
        # Contrôle que l'auteur est un contributeur du projet associée à l'issue
        project = serializer.validated_data.get('project')
        if not Contributor.objects.filter(user=self.request.user, project=project).exists():
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Vous devez être contributeur du projet pour créer une issue.")
        serializer.save(author=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsProjectContributor, IsAuthorOrReadOnly, IsContributorCreatePermission]

    def perform_create(self, serializer):
        issue = serializer.validated_data.get('issue')
        project = issue.project
        if not Contributor.objects.filter(user=self.request.user, project=project).exists():
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Vous devez être contributeur du projet pour commenter une issue.")
        serializer.save(author=self.request.user)

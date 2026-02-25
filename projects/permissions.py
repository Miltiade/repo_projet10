from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsProjectContributor(BasePermission):
    """
    Autorise uniquement l'accès aux contributeurs (y compris l'auteur) du projet
    associé à l'objet considéré.
    """
    def has_object_permission(self, request, view, obj):
        # Identifie le projet lié à l'objet
        if hasattr(obj, 'project'):
            project = obj.project
        elif hasattr(obj, 'issue'):
            project = obj.issue.project
        else:
            return False  # Pas de projet, accès refusé

        user = request.user
        # Vérifie que l'utilisateur est contributeur ou auteur du projet
        is_contributor = project.contributors.filter(user=user).exists()
        is_author = project.author == user
        return is_contributor or is_author


class IsAuthorOrReadOnly(BasePermission):
    """
    Seul l'auteur d'un objet peut modifier ou supprimer, les autres ont accès en lecture seule.
    S'applique aux ressources ayant un champ 'author'.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:  # GET, HEAD, OPTIONS
            return True
        return getattr(obj, 'author', None) == request.user


class IsContributorCreatePermission(BasePermission):
    """
    Autorise seulement les contributeurs à créer une ressource liée à un projet.
    Utilisé dans has_permission, car pas d'objet encore.
    """
    def has_permission(self, request, view):
        if request.method != 'POST':
            return True  # Pas de restriction pour autres méthodes ici

        project_id = request.data.get('project')
        if not project_id:
            return False  # Le projet doit être précisé dans la requête

        from projects.models import Project
        try:
            project = Project.objects.get(pk=project_id)
        except Project.DoesNotExist:
            return False

        user = request.user
        is_contributor = project.contributors.filter(user=user).exists()
        is_author = project.author == user
        return is_contributor or is_author
from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAuthorOrReadOnly(BasePermission):
    """
    Permission qui autorise uniquement l’auteur à modifier une ressource,
    tandis que les autres utilisateurs n’ont qu’un accès en lecture.
    """

    def has_object_permission(self, request, view, obj):
        # Autorise la lecture pour toutes les requêtes sûres (GET, HEAD, OPTIONS)
        if request.method in SAFE_METHODS:
            return True

        # Autorise les opérations d’écriture seulement si l’auteur est le demandeur
        return obj.author == request.user

class IsAuthorOrReadOnlyForAssignee(BasePermission):
    """
    Seul l'auteur d'une issue peut en modifier l'assigné, les autres ont uniquement lecture seule.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        # Interdire modification si pas auteur et changement sur assignee
        if 'assignee' in request.data:
            return obj.author == request.user
        return True
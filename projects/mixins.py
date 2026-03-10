class ContributorProjectQuerySetMixin:
    """
    Mixin qui filtre le queryset pour ne retourner que les objets liés
    à des projets où l'utilisateur est contributeur.
    """
    def get_queryset(self):
        user = self.request.user
        base_qs = super().get_queryset()
        model = base_qs.model

        if hasattr(model, 'project'):
            # Cas général où l'objet est lié directement à un projet
            return base_qs.filter(project__contributors__user=user)
        elif hasattr(model, 'issue'):
            # Cas des commentaires liés à une issue, donc indirectement à un projet
            return base_qs.filter(issue__project__contributors__user=user)
        else:
            # Pas de relation claire, on refuse l'accès
            return base_qs.none()
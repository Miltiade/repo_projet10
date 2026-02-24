from rest_framework import routers
from .views import ProjectViewSet, ContributorViewSet, IssueViewSet, CommentViewSet

router = routers.DefaultRouter()
router.register(r'projects', ProjectViewSet)
router.register(r'contributors', ContributorViewSet)
router.register(r'issues', IssueViewSet)
router.register(r'comments', CommentViewSet)

urlpatterns = router.urls
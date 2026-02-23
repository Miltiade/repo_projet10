from rest_framework import routers
from .views import ProjectViewSet, ContributorViewSet

router = routers.DefaultRouter()
router.register(r'projects', ProjectViewSet)
router.register(r'contributors', ContributorViewSet)

urlpatterns = router.urls
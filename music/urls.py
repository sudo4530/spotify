from django.urls import path, include
from .views import ArtistAPIView, SongSetAPIView, AlbomAPIViewSet
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views

router = DefaultRouter()
router.register("alboms", viewset=AlbomAPIViewSet)
router.register("songs", viewset=SongSetAPIView)
urlpatterns = [
    path("artist/", ArtistAPIView.as_view(), name='artists'),
    path("", include(router.urls)),
    path("auth/", views.obtain_auth_token),
]
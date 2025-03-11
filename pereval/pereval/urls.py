from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, CoordsViewSet, PerevalViewSet, ImageViewSet, PerevalCreateAPIView, SubmitDataViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'coords', CoordsViewSet)
router.register(r'perevals', PerevalViewSet)
router.register(r'images', ImageViewSet)
router.register(r'submitData', SubmitDataViewSet, basename='submit-data')

urlpatterns = [
    path('', include(router.urls)),
    path('pereval/create/', PerevalCreateAPIView.as_view(), name='pereval-create'),  # Маршрут для APIView
]
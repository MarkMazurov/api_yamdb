from django.urls import include, path
from rest_framework import routers

from .views import GenreViewSet, CategoryViewSet, TitleViewSet


router_v1 = routers.DefaultRouter()
router_v1.register(r'categories', CategoryViewSet)
router_v1.register(r'genres', GenreViewSet)
router_v1.register(r'titles', TitleViewSet)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]

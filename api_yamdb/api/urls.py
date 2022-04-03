from rest_framework import routers

from django.urls import include, path

from users.views import UserViewSet, authenticate_user, get_confirmation_code

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('singup/', authenticate_user),
    path('tokenn/', get_confirmation_code),

]

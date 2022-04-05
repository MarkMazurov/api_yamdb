from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework import routers

from users.views import Custom_TokenObtainPairView, get_confirmation_code, \
    UserViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    path(r'admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('auth/singup/', get_confirmation_code),
    path('auth/token/', Custom_TokenObtainPairView.as_view()),

    path(
        'redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),
]

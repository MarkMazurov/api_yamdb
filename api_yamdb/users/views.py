from django.conf import settings
from django.utils.crypto import get_random_string
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view, permission_classes
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, viewsets, mixins
from rest_framework_simplejwt.views import TokenObtainPairView, TokenViewBase

from users.models import CustomUser
from users.permissions import AdminOnly
from users.serializers import UserSerializer, CustomTokenSerializer, \
    UserRegistationSerializer


class CreateOnlyModelViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    pass


class UserViewSet(viewsets.ModelViewSet):
    """CRUD user models"""
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AdminOnly,)
    filter_backends = [DjangoFilterBackend, SearchFilter, ]
    search_fields = ['username']

    def perform_create(self, serializer):
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenSerializer


@api_view(['POST'])
@permission_classes([AllowAny, ])
def get_confirmation_code(request):
    """
    Получить код подтверждения и пароль на переданный email.
    Поля email и username должны быть уникальными.
    """
    serializer = UserRegistationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = CustomUser.objects.create(
        username=serializer.validated_data['username'],
        email=serializer.validated_data['email'],
    )
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789'
    confirmation_code = get_random_string(18, chars)
    user.set_confirmation_code(confirmation_code=confirmation_code)
    user.set_password_code(password=confirmation_code)
    user.save()
    user.email_user(
        subject='Создан confirmation code для получения token',
        message=f'Ваш confirmation code: {confirmation_code}',
        from_email=settings.EMAIL_HOST_USER,
    )
    return Response(serializer.validated_data, status=status.HTTP_200_OK)


class Custom_TokenObtainPairView(TokenViewBase):
    """Получение токена взамен username и confirmation code."""
    serializer_class = CustomTokenSerializer
    permission_classes = (AllowAny,)

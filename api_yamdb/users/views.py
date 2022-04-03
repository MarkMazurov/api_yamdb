import jwt
from django.conf import settings
from django.contrib.auth import get_user_model, user_logged_in
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, viewsets, mixins
from rest_framework_jwt.serializers import jwt_payload_handler

from users.models import CustomUser
from users.permissions import UserOrReadOnly
from users.serializers import UserSerializer, GetTokenSerializer


class CreateOnlyModelViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    pass


class UserViewSet(viewsets.ModelViewSet):
    """CRUD user models"""
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # def post(self, request):
    #     user = request.data
    #     serializer = UserSerializer(data=user)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)


# class ActivateTokenViewSet(CreateOnlyModelViewSet):
#     serializer_class = GetTokenSerializer
#     permission_classes = (AllowAny,)
#
#     def perform_create(self, serializer):
#         username = serializer.data['username']
#         confirmation_code = serializer.data['confirmation_code']
#         user = CustomUser.objects.get(username=username,
#                                       confirmation_code=confirmation_code)
#         try:
#             if user:
#                 try:
#                     payload = jwt_payload_handler(user)
#                     token = jwt.encode(payload, settings.SECRET_KEY)
#                     user_details = {
#                         'username': user.username,
#                         'token': token
#                     }
#                     user_logged_in.send(sender=user.__class__,
#                                         request=self.request, user=user)
#                     return Response(user_details, status=status.HTTP_200_OK)
#                 except Exception as e:
#                     raise e
#             else:
#                 response = {
#                     'error': 'can not authenticate with the given '
#                              'credentials or the account has been '
#                              'deactivated'}
#                 return Response(response, status=status.HTTP_403_FORBIDDEN)
#         except KeyError:
#             response = {
#                 'error': 'please provide a username and a confirmation_code'}
#             return Response(response)

@api_view(['POST'])
@permission_classes([AllowAny, ])
def authenticate_user(request):
    try:
        username = request.data['username']
        confirmation_code = request.data['confirmation_code']
        user = CustomUser.objects.get(username=username, confirmation_code=confirmation_code)
        if user:
            try:
                payload = jwt_payload_handler(user)
                token = jwt.encode(payload, settings.SECRET_KEY)
                user_details = {
                    'username': user.username,
                    'token': token
                }
                user_logged_in.send(sender=user.__class__,
                                    request=request, user=user)
                return Response(user_details, status=status.HTTP_200_OK)
            except Exception as e:
                raise e
        else:
            res = {
                'error': 'can not authenticate with the given credentials or the account has been deactivated'}
            return Response(res, status=status.HTTP_403_FORBIDDEN)
    except KeyError:
        res = {'error': 'please provide a username and a confirmation_code'}
        return Response(res)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_confirmation_code(request):
    '''
    Получить код подтверждения на переданный email.
    Права доступа: Доступно без токена.
    Использовать имя 'me' в качестве username запрещено.
    Поля email и username должны быть уникальными.
    '''
    serializer = UserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    _user = CustomUser.objects.create(
        username=serializer.validated_data['username'],
        email=serializer.validated_data['email'],
    )
    payload = jwt_payload_handler(_user)
    confirmation_code = jwt.encode(payload, settings.SECRET_KEY)
    _user.set_confirmation_code(confirmation_code=confirmation_code)
    _user.save()
    _user.email_user(
        subject='Создан confirmation code для получения token',
        message=f'Ваш confirmation code {confirmation_code}',
        from_email=settings.EMAIL_HOST_USER,
    )
    return Response(serializer.validated_data, status=status.HTTP_200_OK)

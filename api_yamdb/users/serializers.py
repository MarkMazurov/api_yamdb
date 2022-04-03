from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator


from users.models import CustomUser

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'email')
        extra_kwargs = {'password': {'write_only': True},
                        'confirmation_code': {'write_only': True}
                        }
        read_only_fields = ['role']
        validators = [
            UniqueTogetherValidator(
                queryset=CustomUser.objects.all(),
                fields=['username', 'email']
            )
        ]

    def validate_username(self, value):
        if value.lower() == ('me' * (len(value) // 2)):
            raise serializers.ValidationError(
                f'Имя {value} не может быть использованно')
        return value


class GetTokenSerializer(serializers.ModelSerializer):
    pass


# class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
#     # Allow only authenticated users to access this url
#     permission_classes = (IsAuthenticated,)
#     serializer_class = UserSerializer
#
#     def get(self, request, *args, **kwargs):
#         # serializer to handle turning our `User` object into something that
#         # can be JSONified and sent to the client.
#         serializer = self.serializer_class(request.user)
#
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     def put(self, request, *args, **kwargs):
#         serializer_data = request.data.get('user', {})
#
#         serializer = UserSerializer(
#             request.user, data=serializer_data, partial=True
#         )
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#
#         return Response(serializer.data, status=status.HTTP_200_OK)


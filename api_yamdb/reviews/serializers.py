from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Category, Comment, Genre, Review, Title

User = get_user_model()


class ReviewSerializer(serializers.ModelSerializer):
    reviewed_item = serializers.PrimaryKeyRelatedField(read_only=True)
    # author = serializers.SlugRelatedField(
    #     read_only=True, slug_field='username',
    #     default=serializers.CurrentUserDefault()
    # )

    class Meta:
        fields = '__all__'
        model = Review
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=[
                    'reviewed_item',
                    'item_rating',
                    # 'author'
                ]
            ),
        ]


class CommentSerializer(serializers.ModelSerializer):
    review = serializers.PrimaryKeyRelatedField(read_only=True)
    # author = serializers.SlugRelatedField(
    #     read_only=True, slug_field='username',
    #     default=serializers.CurrentUserDefault()
    # )

    class Meta:
        fields = '__all__'
        model = Comment

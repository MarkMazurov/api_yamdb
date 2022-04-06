import datetime as dt

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.serializers import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Title, Category, Comment, Genre, Review

User = get_user_model()


class GenreSerializer(serializers.ModelSerializer):
    # удаление жанра или категории происходит только через указание
    # Id объекта, а не через поле slug. Надо решить этот вопрос!

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')


class TitleListSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        model = Title
        fields = '__all__'


class TitleSerializer(serializers.ModelSerializer):
    genre = SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )
    category = SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    description = serializers.CharField(required=False)

    class Meta:
        model = Title
        fields = '__all__'

    def validate_year(self, value):
        year = dt.date.today().year
        if year < value:
            raise serializers.ValidationError(
                'Проверьте год создания произведения!'
            )
        return value


class ReviewSerializer(serializers.ModelSerializer):
    reviewed_item = serializers.PrimaryKeyRelatedField(read_only=True)
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        fields = '__all__'
        model = Review
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=[
                    'reviewed_item',
                    'item_rating',
                    'author'
                ]
            ),
        ]


class CommentSerializer(serializers.ModelSerializer):
    review = serializers.PrimaryKeyRelatedField(read_only=True)
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        fields = '__all__'
        model = Comment

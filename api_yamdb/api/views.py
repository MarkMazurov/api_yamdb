from rest_framework import filters, mixins, permissions, serializers, viewsets
from rest_framework.permissions import AllowAny

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from reviews.models import Category, Genre, Review, Title
from users.permissions import (AdminOnly, ModeratorOnly, UserOnly,
                               ReadOrAdminOnly, AuthorOrAdminOrModeratorOnly)
from .filters import TitleFilter
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer,
                          TitleSerializer, TitleListSerializer)

User = get_user_model()


class ListCreateDestViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                            mixins.DestroyModelMixin, viewsets.GenericViewSet):
    pass


class GenreViewSet(ListCreateDestViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [ReadOrAdminOnly]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class CategoryViewSet(ListCreateDestViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [ReadOrAdminOnly]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = [ReadOrAdminOnly]
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return TitleListSerializer
        return TitleSerializer

    # def get_serializer_class(self):
    #    if self.action == 'list' or self.action == 'retrieve':
    #        return TitleListSerializer
    #    return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [AuthorOrAdminOrModeratorOnly]
    permission_classes_by_action = {'list': [AllowAny],
                                    'create': [
                                        AdminOnly | ModeratorOnly | UserOnly]}

    def get_queryset(self):
        current_title = get_object_or_404(
            Title, pk=self.kwargs.get('title_id')
        )
        return current_title.reviews.all()

    def perform_create(self, serializer):
        current_title = get_object_or_404(
            Title, pk=self.kwargs.get('title_id')
        )
        author = self.request.user
        if Review.objects.filter(author=author, title=current_title).exists():
            raise serializers.ValidationError(
                "Вами уже был оставлен отзыв на это произведение")
        serializer.save(author=author, title=current_title)

    def get_permissions(self):
        try:
            return [permission() for permission
                    in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [AuthorOrAdminOrModeratorOnly]
    permission_classes_by_action = {'list': [AllowAny],
                                    'create': [
                                        AdminOnly | ModeratorOnly | UserOnly]}

    def get_queryset(self):
        current_review = get_object_or_404(
            Review, pk=self.kwargs.get('review_id')
        )
        return current_review.comments.all()

    def perform_create(self, serializer):
        title = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id, title__id=title)
        serializer.save(author=self.request.user, review=review)

    def get_permissions(self):
        try:
            return [permission() for permission
                    in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]

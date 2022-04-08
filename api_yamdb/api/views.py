from rest_framework import filters, mixins, permissions, viewsets
from rest_framework.permissions import AllowAny

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from reviews.models import Category, Genre, Review, Title
from users.permissions import (AdminOnly, ModeratorOnly, UserOnly,
                               AuthorOrAdminOrModeratorOnly, ReadOrAdminOnly)
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
                                        AdminOnly | ModeratorOnly | UserOnly],
                                    'retrieve': [AllowAny],
                                    'partial_update': [
                                        AuthorOrAdminOrModeratorOnly],
                                    'destroy': [AuthorOrAdminOrModeratorOnly]}

    def get_queryset(self):
        current_title = get_object_or_404(
            Title, pk=self.kwargs.get('title_id')
        )
        return current_title.reviews.all()

    def perform_create(self, serializer):
        reviewed_item = get_object_or_404(
            Title, pk=self.kwargs.get('title_id')
        )
        serializer.save(author=self.request.user, reviewed_item=reviewed_item)

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
                                        AdminOnly | ModeratorOnly | UserOnly],
                                    'retrieve': [AllowAny],
                                    'partial_update': [
                                        AuthorOrAdminOrModeratorOnly],
                                    'destroy': [AuthorOrAdminOrModeratorOnly]}

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

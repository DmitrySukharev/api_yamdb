from rest_framework import filters, mixins, viewsets
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404

from reviews.models import Category, Genre, Title, Review
from .serializers import CategorySerializer, GenreSerializer
from .serializers import ReviewSerializer, CommentsSerializer


class ListCreateDestroyViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):
    pass


class ListCreateUpdateDestroyViewSet(mixins.ListModelMixin,
                                     mixins.CreateModelMixin,
                                     mixins.UpdateModelMixin,
                                     mixins.DestroyModelMixin,
                                     viewsets.GenericViewSet):
    pass


class CategoryViewSet(ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class ReviewViewSet(ListCreateUpdateDestroyViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get("title_id"))
        new_queryset = title.reviews.all()
        return new_queryset

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get("title_id"))
        serializer.save(author=self.request.user, title=title)


class CommentsViewSet(ListCreateUpdateDestroyViewSet):
    serializer_class = CommentsSerializer

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get("review_id"))
        new_queryset = review.comments.all()
        return new_queryset

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get("review_id"))
        serializer.save(author=self.request.user, review=review)

from django_filters import CharFilter, FilterSet, NumberFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, mixins, status, viewsets
from rest_framework.response import Response

from reviews.models import Category, Genre, Title
from .permissions import AdminOrReadOnly
from .serializers import CategorySerializer, GenreSerializer
from .serializers import TitleReadSerializer, TitleWriteSerializer


class ListCreateDestroyViewSet(mixins.ListModelMixin,
                               mixins.CreateModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):
    pass


class RetrievePatchDestroyAPIView(mixins.RetrieveModelMixin,
                                  mixins.UpdateModelMixin,
                                  mixins.DestroyModelMixin,
                                  generics.GenericAPIView):
    """Concrete view for retrieving, patching or deleting a model instance."""
    # Similar to the built-in APIView but w/o PUT method support
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class CategoryViewSet(ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitleFilter(FilterSet):
    name = CharFilter(field_name='name', lookup_expr='icontains')
    year = NumberFilter(field_name='year')
    category = CharFilter(field_name='category__slug')
    genre = CharFilter(field_name='genre__slug')

    class Meta:
        model = Title
        fields = ['name', 'year', 'genre', 'category']


class TitleList(generics.ListCreateAPIView):
    queryset = Title.objects.all()
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleReadSerializer
        return TitleWriteSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        # Используем новый сериализатор (для чтения), чтобы вернуть
        # объекты категорий и жанров вместо slug-ов
        new_title_id = serializer.data['id']
        new_title = Title.objects.get(id=new_title_id)
        new_serializer = TitleReadSerializer(new_title)
        return Response(
            new_serializer.data,
            status=status.HTTP_201_CREATED, headers=headers
        )


class TitleDetail(RetrievePatchDestroyAPIView):
    queryset = Title.objects.all()
    permission_classes = (AdminOrReadOnly,)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleReadSerializer
        return TitleWriteSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        new_serializer = TitleReadSerializer(instance)
        return Response(new_serializer.data)

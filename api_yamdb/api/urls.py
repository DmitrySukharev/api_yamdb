from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, GenreViewSet, TitleDetail, TitleList

router_1 = DefaultRouter()
router_1.register('v1/categories', CategoryViewSet)
router_1.register('v1/genres', GenreViewSet)

urlpatterns = [
    path('', include(router_1.urls)),
    path('v1/titles/', TitleList.as_view(), name='title-list'),
    path('v1/titles/<int:pk>/', TitleDetail.as_view(), name='title-detail'),
]

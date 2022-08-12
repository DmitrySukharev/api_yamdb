from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CategoryViewSet, GenreViewSet
from .views import ReviewViewSet, CommentsViewSet

router_1 = DefaultRouter()
router_1.register('v1/categories', CategoryViewSet)
router_1.register('v1/genres', GenreViewSet)
router_1.register(r'v1/titles/(?P<title_id>\d+)/reviews', ReviewViewSet,
                  basename='reviews')
router_1.register(
    r'v1/titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentsViewSet,
    basename='comments')

urlpatterns = [
    path('', include(router_1.urls)),
    # path('v1/follow/', FollowListCreate.as_view(), name='follow'),
]

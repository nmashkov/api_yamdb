from django.urls import include, path
from rest_framework.routers import DefaultRouter

from reviews.views import ReviewViewSet, CommentViewSet
from titles.views import CategoryViewSet, TitleViewSet, GenreViewSet


app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)'r'/comments',
    CommentViewSet,
    basename='comments')
router_v1.register(
    'categories',
    CategoryViewSet,
    basename='сategories'
)
router_v1.register(
    'titles',
    TitleViewSet,
    basename='titles'
)
router_v1.register(
    'genres',
    GenreViewSet,
    basename='genres'
)

urlpatterns = [
    path('v1/', include('users.urls', namespace='users')),
    path('v1/', include(router_v1.urls)),
]

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from reviews.views import ReviewViewSet, CommentViewSet


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

urlpatterns = [
    path('v1/auth/', include('users.urls', namespace='users')),
    path('v1/', include(router_v1.urls)),
]

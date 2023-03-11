from django.urls import path, include
from rest_framework.routers import DefaultRouter

from reviews.views import ReviewViewSet, CommentViewSet


app_name = 'reviews'

router_reviews = DefaultRouter()
router_reviews.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews')
router_reviews.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)'r'/comments',
    CommentViewSet,
    basename='comments')

urlpatterns = [
    path('', include(router_reviews.urls)),
]

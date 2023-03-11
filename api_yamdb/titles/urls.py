from django.urls import path, include
from rest_framework.routers import DefaultRouter

from titles.views import CategoryViewSet, TitleViewSet, GenreViewSet


app_name = 'titles'

router_titles = DefaultRouter()
router_titles.register(
    'categories',
    CategoryViewSet,
    basename='сategories'
)
router_titles.register(
    'titles',
    TitleViewSet,
    basename='titles'
)
router_titles.register(
    'genres',
    GenreViewSet,
    basename='genres'
)

urlpatterns = [
    path('', include(router_titles.urls)),
]

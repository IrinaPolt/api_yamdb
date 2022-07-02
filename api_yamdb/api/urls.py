from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import SignUpApiView, GenerateToken, \
    UserViewSet, ReviewViewSet, CommentViewSet
from .views import (
    CategoriesViewSet,
    GenresViewSet,
    TitlesViewSet
)

app_name = 'api'

router = DefaultRouter()

router.register(r'users', UserViewSet)
router.register(r'categories', CategoriesViewSet, basename='categories')
router.register(r'genres', GenresViewSet, basename='genres')
router.register(r'titles', TitlesViewSet, basename='titles')
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename="reviews",
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments',
)


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', SignUpApiView.as_view()),
    path('v1/auth/token/', GenerateToken.as_view()),
]

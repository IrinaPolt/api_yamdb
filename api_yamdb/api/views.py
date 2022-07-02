import random
import string
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, mixins, filters
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from django.db.models import Avg

from api.permissions import IsAdmin, IsAdminOrReadOnly, \
    AuthorModeratorOrReadOnly
from api.serializers import (
    SignUpSerializer,
    UserSerializer,
    UserEditSerializer,
    GenerateTokenSerializer,
    CategoriesSerializer,
    GenresSerializer,
    TitlesReadSerializer,
    TitlesCreateSerializer, ReviewSerializer, CommentSerializer
)
from .filters import TitlesFilter
from reviews.models import User, Category, Genre, Title, Review


def generate_confirmation_code():
    confirmation_code = ''.join(
        random.choice(string.digits) for x in range(6))
    return confirmation_code


class SignUpApiView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        confirmation_code = generate_confirmation_code()
        serializer.validated_data['confirmation_code'] = confirmation_code
        serializer.save()
        user = get_object_or_404(User, username=serializer.data['username'])
        message = (
            f'Для продолжения регистрации введите код подтверждения:'
            f'{confirmation_code}'
        )
        send_mail(
            subject='Welcome to YaMDb',
            message=message,
            from_email=None,
            recipient_list=[user.email],
            fail_silently=False
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class GenerateToken(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = GenerateTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(User, username=serializer.validated_data[
            'username'])
        code = user.confirmation_code
        if code == serializer.validated_data['confirmation_code']:
            token = AccessToken.for_user(user)
            return Response({'token': str(token)}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    lookup_field = 'username'
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsAdmin,)

    @action(
        methods=[
            'GET',
            'PATCH',
        ],
        detail=False,
        url_path='me',
        permission_classes=(IsAuthenticated,),
        serializer_class=UserEditSerializer,
    )
    def users_me_profile(self, request):
        user = request.user
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == 'PATCH':
            serializer = self.get_serializer(
                user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class YamdbMixin(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """Кастомный миксин для наследования вьюсетами."""
    pass


class CategoriesViewSet(YamdbMixin):
    """Обработка категории."""
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer
    pagination = PageNumberPagination
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenresViewSet(YamdbMixin):
    """Обработка жанра."""
    queryset = Genre.objects.all()
    serializer_class = GenresSerializer
    pagination = PageNumberPagination
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitlesViewSet(viewsets.ModelViewSet):
    """Обработка произведения."""
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    ).all().order_by('name')
    serializer_class = TitlesReadSerializer
    pagination = PageNumberPagination
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_class = TitlesFilter

    def get_serializer_class(self):
        """Выбор сериализатора для необходимого запроса."""
        if self.action in ('list', 'retrieve'):
            return TitlesReadSerializer
        return TitlesCreateSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (AuthorModeratorOrReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (AuthorModeratorOrReadOnly,)

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)

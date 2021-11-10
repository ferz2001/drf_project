from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import filters

from backend.models import (Categorie,
                            Genre,
                            Title,
                            Review,
                            Comment,
                            User)
from .serializers import (UserSerializer,
                          CategorieSerializer,
                          GenreSerializer,
                          TitleSerializer,
                          ReviewSerializer,
                          CommentSerializer)

from .utilities import get_confirmation_code, send_confirmation_code_email


class RegisterView(APIView):

    def post(self, request):
        email = request.data.get('email')
        confirmation_code = get_confirmation_code()
        data = {'email': email, 'confirmation_code': confirmation_code,}
        serializer = UserSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        send_confirmation_code_email(email, confirmation_code)
        return Response(serializer, status=status.HTTP_200_OK)


class TokenView(APIView):
    def get_token(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def post(self, request):
        email = request.data.get('email')
        user = get_object_or_404(User, email=email)
        if user.confirmation_code != request.data.get('confirmation_code'):
            response = {'confirmation_code': 'Invalid confirmation code'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        response = {'token': self.get_token(user)}
        return Response(response, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter, )
    search_field = 'username'


class CategorieViewSet(viewsets.ModelViewSet):
    queryset = Categorie.objects.all()
    serializer_class = CategorieSerializer


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = LimitOffsetPagination


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (filters.SearchFilter, )
    search_fields = ('category', 'genre', 'name', 'year')


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category', 'genre', 'name', 'year')

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        super(CommentViewSet, self).perform_update(serializer)

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        super(CommentViewSet, self).perform_destroy(instance)

    def get_queryset(self):
        title_id = self.kwargs['title_id']
        title = get_object_or_404(Title, id=title_id)
        return title.reviews

    def perform_create(self, serializer):
        title_id = self.kwargs['title_id']
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user,
                        title=title)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        super(CommentViewSet, self).perform_update(serializer)

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        super(CommentViewSet, self).perform_destroy(instance)

    def get_queryset(self):
        review_id = self.kwargs['review_id']
        review = get_object_or_404(Review, id=review_id)
        return review.comments

    def perform_create(self, serializer):
        title_id = self.kwargs['title_id']
        review_id = self.kwargs['review_id']
        title = get_object_or_404(Title, id=title_id)
        review = get_object_or_404(Review, id=review_id)
        serializer.save(author=self.request.user,
                        title=title,
                        review=review)

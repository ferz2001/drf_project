from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status, viewsets, permissions, mixins
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import filters
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
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
from .permissions import (IsAdmin, IsAdminOrReadOnly, IsAuthor, IsModerator,
                          IsSuperuser)

class RegisterView(APIView):
    permission_classes = (AllowAny,)
    def post(self, request):
        email = request.data.get('email')
        username = request.data.get('username')
        confirmation_code = get_confirmation_code()
        data = {
            'email': email,
            'username': username,
            'confirmation_code': confirmation_code
        }
        serializer = UserSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        send_confirmation_code_email(email, confirmation_code)
        return Response(serializer, status=status.HTTP_200_OK)


class TokenView(APIView):
    permission_classes = (AllowAny,)
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
    permission_classes = (IsAuthenticated, IsSuperuser | IsAdmin,)

    @action(detail=False, permission_classes=(permissions.IsAuthenticated,),
            methods=['GET', 'PATCH'], url_path='me')
    def get_or_patch_yourself(self, request):
        if request.method == 'GET':
            serializer=self.get_serializer(request.user, many=False)
            return Response(serializer.data)
        elif request.method == 'PATCH':
            serializer = self.get_serializer(instance=request.user,
                                    data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)



class CategorieViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                       mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Categorie.objects.all()
    serializer_class = CategorieSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name',)
    permission_classes = [IsAdminOrReadOnly]

    def perform_create(self, serializer):
        if self.request.user.role == 'ADMIN':
            serializer.save()
        else:
            raise PermissionDenied(
                'Только администратор имеет право добавлять новые категории')

    def perform_destroy(self, instance):
        if self.request.user.role == 'ADMIN':
            super(CategorieViewSet, self).perform_destroy(instance)
        else:
            raise PermissionDenied(
                'Только администратор имеет право удалять категории')


class GenreViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                   mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = LimitOffsetPagination
    search_fields = ('name',)
    permission_classes = [IsAdminOrReadOnly]

    def perform_create(self, serializer):
        if self.request.user.role == 'ADMIN':
            serializer.save()
        else:
            raise PermissionDenied(
                'Только администратор имеет право добавлять новые жанры')

    def perform_destroy(self, instance):
        if self.request.user.role == 'ADMIN':
            super().perform_destroy(instance)
        else:
            raise PermissionDenied(
                'Только администратор имеет право удалять жанры')


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter, DjangoFilterBackend,)
    filterset_fields = ('categorie', 'genre__slug', 'name', 'year')
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]

    def perform_create(self, serializer):
        if 'categorie' not in serializer.initial_data:
            text_error = ('Назвние категории произведения'
                          ' обязательно должно присутсвовать')
            raise PermissionDenied(text_error)
        if 'genre' not in serializer.initial_data:
            text_error = ('Назвние жанра произведения'
                          ' обязательно должно присутсвовать')
            raise PermissionDenied(text_error)
        categorie = serializer.initial_data['categorie']
        genre = serializer.initial_data['genre']
        if self.request.user.role == 'ADMIN':
            get_object_or_404(Categorie, id=categorie)
            get_object_or_404(Genre, id=genre)
            serializer.save()
        else:
            raise PermissionDenied('Только администратор имеет'
                                   ' право добавлять новые произведения')

    def perform_update(self, serializer):
        if 'categorie' in serializer.initial_data:
            categorie = serializer.initial_data['categorie']
            get_object_or_404(Categorie, id=categorie)
        if 'genre' in serializer.initial_data:
            genre = serializer.initial_data['genre']
            get_object_or_404(Genre, id=genre)
        if self.request.user.role == 'ADMIN':
            serializer.save()
        else:
            raise PermissionDenied('Только администратор имеет'
                                   ' право обновлять данные о произведении')

    def perform_destroy(self, instance):
        if self.request.user.role == 'ADMIN':
            super().perform_destroy(instance)
        else:
            raise PermissionDenied(
                'Только администратор имеет право удалять произведения')


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthor | IsModerator |
                          IsAdminOrReadOnly | IsSuperuser]

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
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthor | IsModerator |
                          IsAdminOrReadOnly | IsSuperuser]

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

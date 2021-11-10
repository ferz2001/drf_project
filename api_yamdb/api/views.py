from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from backend.models import User
from backend.serializers import UserSerializer
from .utilities import get_confirmation_code, send_confirmation_code_email


class RegisterView(APIView):
    def post(self, request):
        email=request.data.get('email')
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
        response= {'token': self.get_token(user)}
        return Response(response, status=status.HTTP_200_OK)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
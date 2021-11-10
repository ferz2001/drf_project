from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import RegisterView, TokenView, UserViewSet

app_name = 'api'

api_router = DefaultRouter()
api_router.register('users', UserViewSet, basename='users')
urlpatterns = [
    path('v1/auth/signup/', RegisterView.as_view(), name='register'),
    path('v1/auth/token/', TokenView.as_view(), name='get_token'),
    path('v1/', include(api_router.urls)),
]
from django.urls import include, path

from .views import RegisterView, TokenView

app_name = 'api'

urlpatterns = [
    path('v1/auth/signup/', RegisterView.as_view()),
    path('v1/auth/token/', TokenView.as_view()),
]
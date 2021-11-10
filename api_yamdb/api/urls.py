from django.urls import include, path

from .views import RegisterView

app_name = 'api'

urlpatterns = [
    path('/auth/signup/'), RegisterView.as_view(),
]

from django.urls import path, include
from .views import *

urlpatterns = [
    path('api/v1/movie', MovieListView.as_view()),
    path('api/v1/auth', include('djoser.urls')),
    path('api/v1/', include('djoser.urls.authtoken')),
    path('movie/<int:pk>', MovieDetail.as_view()),
    path('review/', ReviewCreateView.as_view()),
    path('create/movie/', CreateMovieView.as_view())
]

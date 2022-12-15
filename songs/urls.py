from django.urls import path

from .views import SongView

urlpatterns = [
    path("albums/<int:pk>/songs/", SongView.as_view()),
]

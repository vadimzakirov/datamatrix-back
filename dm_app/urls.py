from django.urls import path
from .views import SessionGenerator, ImageWorker

urlpatterns = [
    path('session/', SessionGenerator.as_view()),
    path('get_images/', ImageWorker.as_view())
]

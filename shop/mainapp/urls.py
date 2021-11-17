from django.urls import path

from .views import test_view, DogDetailView

urlpatterns = [
    path('', test_view, name='base'),
    path('dogs/<str:ct_model>/<str:slug>/', DogDetailView.as_view(), name='dog_detail')
]  # http://127.0.0.1:8000/dogs/our/AdultDog/ - result: Адель

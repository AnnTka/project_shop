from django.urls import path

from .views import test_view, DogDetailView, CategoryDetailView

urlpatterns = [
    path('', test_view, name='base'),
    path('dogs/<str:ct_model>/<str:slug>/', DogDetailView.as_view(), name='dog_detail'),
    # http://127.0.0.1:8000/dogs/our/Adel/ - result: Адель
    path('category/<str:slug>/', CategoryDetailView.as_view(), name='category_detail')
]

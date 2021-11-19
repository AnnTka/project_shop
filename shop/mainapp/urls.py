from django.urls import path
from .views import BaseView, DogDetailView, CategoryDetailView, LoginView, RegistrationView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', BaseView.as_view(), name='base'),
    path('dogs/<str:slug>/', DogDetailView.as_view(), name='dog_detail'),
    # http://127.0.0.1:8000/dogs/our/Adel/ - result: Адель
    path('category/<str:slug>/', CategoryDetailView.as_view(), name='category_detail'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page="/"), name='logout'),
    path('registration/', RegistrationView.as_view(), name='registration')
]

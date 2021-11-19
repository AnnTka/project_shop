from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import DetailView, View
from .models import Category, Dog, CartDog, Cart, Customer
from .forms import LoginForm
from django.contrib.auth import authenticate, login


class BaseView(View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        dogs = Dog.objects.all()
        context = {
            'categories': categories,
            'dogs': dogs
        }
        return render(request, 'base.html', context)


# view for handle multiple models with 1 template
class DogDetailView(DetailView):

    context_object_name = 'dog'
    template_name = 'dog_detail.html'
    slug_url_kwarg = 'slug'

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        dogs = Dog.objects.all()
        context = {
            'categories': categories,
            'dogs': dogs
        }
        return render(request, 'dog_detail.html', context)


class CategoryDetailView(DetailView):

    model = Category
    queryset = Category.objects.all()
    context_object_name = 'category'
    template_name = 'category_detail.html'
    slug_url_kwarg = 'slug'


class LoginView(View):

    def get(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        categories = Category.objects.all()
        context = {'form': form, 'categories': categories}
        return render(request, 'login.html', context)

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect('/')
        return render(request, 'login.html', {'form': form})


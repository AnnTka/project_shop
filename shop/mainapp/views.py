from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import DetailView, View
from .models import Category, Dog, CartDog, Cart, Customer
from .forms import LoginForm, RegistrationForm
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
        context = {'form': form}
        return render(request, 'login.html', context)


class RegistrationView(View):

    def get(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        categories = Category.objects.all()
        context = {'form': form, 'categories': categories}
        return render(request, 'registration.html', context)

    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.username = form.cleaned_data['username']
            new_user.email = form.cleaned_data['email']
            new_user.first_name = form.cleaned_data['first_name']
            new_user.last_name = form.cleaned_data['last_name']
            new_user.save()
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            Customer.objects.create(
                user=new_user,
                phone=form.cleaned_data['phone'],
                address=form.cleaned_data['address'],
            )
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            login(request, user)
            return HttpResponseRedirect('/')
        context = {'form': form}
        return render(request, 'registration.html', context)

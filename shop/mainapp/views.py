from django.views.generic import DetailView, View
from .models import Category, Dog
from django.shortcuts import render


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




from django.shortcuts import render
from django.views.generic import DetailView, View

from .models import OurDog, DogForSale, Category, LatestDogs
from .mixins import CategoryDetailMixin


class BaseView(View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.get_sidebar_categories()
        dogs = LatestDogs.objects.get_dog_for_main_page(
            'ourdog', 'dogforsale', with_respect_to='dogforsale'
        )
        context = {
            'categories': categories,
            'dogs': dogs
        }
        return render(request, 'base.html', context)

# def test_view(request):
# categories = Category.objects.get_sidebar_categories()
# return render(request, 'base.html', {'categories': categories})


# view for handle multiple models with 1 template
class DogDetailView(CategoryDetailMixin, DetailView):

    CT_MODEL_MODEL_CLASS = {
        'ourdog': OurDog,
        'dogforsale': DogForSale
    }

    # to define the model and display their objects,
    # so as not to write different url patterns for each model
    def dispatch(self, request, *args, **kwargs):
        self.model = self.CT_MODEL_MODEL_CLASS[kwargs['ct_model']]
        self.queryset = self.model._base_manager.all()
        return super().dispatch(request, *args, **kwargs)

    context_object_name = 'dog'
    template_name = 'dog_detail.html'
    slug_url_kwarg = 'slug'


class CategoryDetailView(CategoryDetailMixin, DetailView):

    model = Category
    queryset = Category.objects.all()
    context_object_name = 'category'
    template_name = 'category_detail.html'
    slug_url_kwarg = 'slug'



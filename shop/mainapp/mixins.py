from django.views.generic.detail import SingleObjectMixin

from .models import Category, OurDog, DogForSale


class CategoryDetailMixin(SingleObjectMixin):

    CATEGORY_SLUG = {
        'ourdog': OurDog,
        'dogforsale': DogForSale
    }

    def get_context_data(self, **kwargs):
        if isinstance(self.get_object(), Category):
            model = self.CATEGORY_SLUG[self.get_object().slug]
            context = super().get_context_data(**kwargs)
            context['categories'] = Category.objects.get_sidebar_categories()
            context['category_dogs'] = model.objects.all()
            return context
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.get_sidebar_categories()
        return context

from django.shortcuts import render
from django.views.generic import DetailView

from .models import OurDog, DogForSale


def test_view(request):
    return render(request, 'base.html', {})


# view for handle multiple models with 1 template
class DogDetailView(DetailView):

    CT_MODEL_MODEL_CLASS = {
        'our': OurDog,
        'sale': DogForSale
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

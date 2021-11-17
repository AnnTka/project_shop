from django.contrib import admin
from django.forms import ModelForm, ValidationError
from .models import *
from PIL import Image


class DogAdminForm(ModelForm):

    MIN_RESOLUTION = (500, 500)
    MAX_RESOLUTION = (2000, 2000)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].help_text = 'Загружайте изображения с минимальным разрешением {}x{}'.format(
            *self.MIN_RESOLUTION
        )

    def clean_image(self):
        image = self.cleaned_data['image']
        img = Image.open(image)
        min_height, min_width = self.MIN_RESOLUTION
        max_height, max_width = self.MAX_RESOLUTION
        if img.height < min_height or img.width < min_width:
            raise ValidationError('Разрешение изображения меньше минимального!')
        if img.height < max_height or img.width < max_width:
            raise ValidationError('Разрешение изображения больше максимального!')
        return image


admin.site.register(CartProduct)
admin.site.register(Cart)
admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(OurDog)
admin.site.register(DogForSale)

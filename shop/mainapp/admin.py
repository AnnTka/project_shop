from django.contrib import admin


# Register your models here.
from .models import *


admin.site.register(CartProduct)
admin.site.register(Cart)
admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(OurDog)
admin.site.register(DogForSale)

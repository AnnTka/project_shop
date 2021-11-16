from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from django.contrib.auth import get_user_model
# settings.AUTH_USER_MODEL
User = get_user_model()


# /categories/adult_dog or puppy == slug
class Category(models.Model):

    name = models.CharField(max_length=255, verbose_name='Имя категории')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Dog(models.Model):

    # abstract model without migration
    class Meta:
        abstract = True

    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name='Наименование')
    slug = models.SlugField(unique=True)
    image = models.ImageField(verbose_name='Фото', null=True)
    breed = models.TextField(max_length=100, verbose_name='Порода')
    color = models.TextField(max_length=255, verbose_name='Окрас')
    gender = models.TextField(max_length=10, verbose_name='Пол')
    age = models.CharField(max_length=2, verbose_name='Возраст')
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='Цена', null=True)

    def __str__(self):
        return self.title


class OurDog(Dog):

    history = models.TextField(max_length=255, verbose_name='История', null=True)  # story about purchasing a pet
    habits = models.TextField(max_length=255, verbose_name='Привычки', null=True)

    def __str__(self):
        return "{} : {}".format(self.category.name, self.title)


class DogForSale(Dog):

    description = models.TextField(max_length=255, verbose_name='Описание', null=True)
    parents = models.TextField(max_length=255, verbose_name='Родители', null=True)  # this is preferably a link

    def __str__(self):
        return "{} : {}".format(self.category.name, self.title)


class CartProduct(models.Model):

    user = models.ForeignKey('Customer', verbose_name='Покупатель', on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', verbose_name='Корзина', on_delete=models.CASCADE, related_name='related_products')
    # p = DogProduct.objects.get(dog1)
    # cp = CartProduct.object.create(content_object=dog1)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)  # autocomplete
    object_id = models.PositiveIntegerField()  # autocomplete
    content_object = GenericForeignKey('content_type', 'object_id')
    qty = models.PositiveIntegerField(default=1)
    final_price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='Итоговая стоимость', null=True)

    def __str__(self):
        return "Покупка: {} (для корзины)".format(self.title)


class Cart(models.Model):

    owner = models.ForeignKey('Customer', verbose_name='Владелец', on_delete=models.CASCADE)
    dog = models.ManyToManyField(CartProduct, blank=True, related_name='related_cart')
    total_products = models.PositiveIntegerField(default=0)
    final_price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='Итоговая стоимость', null=True)

    def __str__(self):
        return str(self.id)


class Customer(models.Model):

    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, verbose_name='Номер телефона')

    def __str__(self):
        return "Покупатель: {} {}".format(self.user.first_name, self.user.last_name)

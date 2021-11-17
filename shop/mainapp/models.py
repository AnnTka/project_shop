from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils import timezone

from django.contrib.auth import get_user_model
# settings.AUTH_USER_MODEL
User = get_user_model()


class LatestDogsManager:
    # for display dogs on the main page
    @staticmethod
    def get_dog_for_main_page(*args, **kwargs):
        with_respect_to = kwargs.get('with_respect_to')  # prioritizing the output of results
        dogs = []
        ct_models = ContentType.objects.filter(model__in=args)
        for ct_model in ct_models:
            model_dogs = ct_model.model_class()._base_manager.all().order_by('-id')[:5]
            dogs.extend(model_dogs)
        if with_respect_to:
            ct_model = ContentType.objects.filter(model=with_respect_to)
            if ct_model.exists():
                if with_respect_to in args:
                    return sorted(
                        dogs, key=lambda x: x.__class__._meta.model_name.startswith(with_respect_to), reverse=True
                    )
        return dogs


class LatestDogs:

    objects = LatestDogsManager()


class Category(models.Model):

    name = models.CharField(max_length=255, verbose_name='Имя категории')
    slug = models.SlugField(unique=True)  # /categories/adult_dog or puppy == slug

    def __str__(self):
        return self.name


class Dog(models.Model):

    # abstract model without migration, parent class
    class Meta:
        abstract = True

    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name='Наименование')
    slug = models.SlugField(unique=True)
    image = models.ImageField(verbose_name='Фото', null=True)
    breed = models.TextField(max_length=100, verbose_name='Порода')
    color = models.TextField(max_length=255, verbose_name='Окрас')
    gender = models.TextField(max_length=10, verbose_name='Пол')
    age = models.TextField(max_length=10, verbose_name='Возраст')
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
    orders = models.ManyToManyField('Order', verbose_name='Заказы покупателя', related_name='related_customer')

    def __str__(self):
        return "Покупатель: {} {}".format(self.user.first_name, self.user.last_name)


class Order(models.Model):

    STATUS_NEW = 'new'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_READY = 'is_ready'
    STATUS_COMPLETED = 'completed'

    BUYING_TYPE_SELF = 'self'
    BUYING_TYPE_DELIVERY = 'delivery'

    STATUS_CHOICES = (
        (STATUS_NEW, 'Новый заказ'),
        (STATUS_IN_PROGRESS, 'Заказ в обработке'),
        (STATUS_READY, 'Заказ готов'),
        (STATUS_COMPLETED, 'Заказ выполнен')
    )

    BUYING_TYPE_CHOICES = (
        (BUYING_TYPE_SELF, 'Самовывоз'),
        (BUYING_TYPE_DELIVERY, 'Доставка')
    )

    customer = models.ForeignKey(Customer, verbose_name='Покупатель', related_name='related_orders', on_delete=models.CASCADE)
    phone = models.CharField(max_length=15,  verbose_name='Номер телефона')
    address = models.CharField(max_length=1024, verbose_name='Адрес', null=True, blank=True)
    status = models.CharField(
        max_length=25, verbose_name='Статус заказа', choices=STATUS_CHOICES, default=STATUS_NEW
    )
    buying_type = models.CharField(
        max_length=25, verbose_name='Тип заказа', choices=BUYING_TYPE_CHOICES, default=BUYING_TYPE_SELF
    )
    comment = models.TextField(verbose_name='Комментарий к заказу', null=True, blank=True)
    created_at = models.DateTimeField(auto_created=True, verbose_name='Дата создания товара')
    order_date = models.DateField(verbose_name='Дата получения заказа', default=timezone.now)

    def __str__(self):
        return str(self.id)

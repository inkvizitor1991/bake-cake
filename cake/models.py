from django.db import models
from django.contrib.auth.models import User

from phonenumber_field.modelfields import PhoneNumberField


class Levels(models.Model):
    """Количество уровней слоев торта. 1, 2, 3 и т.д."""

    quantity = models.IntegerField('количество',  null=True, blank=True)
    price = models.FloatField('цена')

    class Meta:
        verbose_name = 'количество уровней'
        verbose_name_plural = 'количество уровней'

    def __str__(self):
        return str(self.quantity)


class Form(models.Model):
    """Какая у торта будет форма. Круг, квадрат и т.д."""

    figure = models.CharField('фигура', max_length=200)
    price = models.FloatField('цена')

    class Meta:
        verbose_name = 'форма'
        verbose_name_plural = 'формы'

    def __str__(self):
        return self.figure


class Topping(models.Model):
    """Топпинг используемый как ингридиент при приготовлении торта. Карамельный, кленовый и т.д."""

    name = models.CharField('название', max_length=200)
    price = models.FloatField('цена')

    class Meta:
        verbose_name = 'топпинг'
        verbose_name_plural = 'топпинги'

    def __str__(self):
        return self.name


class Berries(models.Model):
    """Ягода используемая как ингридиент при приготовлении торта. Малина, клубника и т.д."""

    name = models.CharField('название', max_length=200)
    price = models.FloatField('цена')

    class Meta:
        verbose_name = 'ягода'
        verbose_name_plural = 'ягоды'

    def __str__(self):
        return self.name


class Decor(models.Model):
    """Декор из продуктов используемый как украшение при приготовлении торта. Фисташки, безе и т.д."""

    name = models.CharField('название', max_length=200)
    price = models.FloatField('цена')

    class Meta:
        verbose_name = 'декор'
        verbose_name_plural = 'декоры'

    def __str__(self):
        return self.name


class Cake(models.Model):
    """Итоговый торт, который получается при смешивании разных ингридиентов."""

    levels = models.ForeignKey(
        Levels,
        verbose_name='количество слоев',
        related_name = 'cake',
        on_delete=models.PROTECT
    )
    form = models.ForeignKey(
        Form,
        verbose_name='форма',
        related_name = 'cake',
        on_delete=models.PROTECT
    )
    topping = models.ForeignKey(
        Topping,
        verbose_name='топпинг',
        related_name = 'cake',
        on_delete=models.PROTECT
    )
    berries = models.ForeignKey(
        Berries,
        verbose_name='ягода',
        related_name = 'cake',
        on_delete=models.PROTECT
    )
    decor = models.ForeignKey(
        Decor,
        verbose_name='декор',
        related_name = 'cake',
        on_delete=models.PROTECT
    )
    words = models.CharField('текст слов на торте', max_length=200)

    class Meta:
        verbose_name = 'торт'
        verbose_name_plural = 'торты'

    def __str__(self):
        return str(self.id)


class Client(models.Model):
    """Зарегистрированный клиент сервиса по заказу тортов."""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = PhoneNumberField("телефон", db_index=True)

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'

    def __str__(self):
        return str(self.phone)


class Delivery(models.Model):
    """Доставка заказанного торта."""

    address = models.TextField("Адрес")
    deliver_at = models.DateTimeField('когда доставить',  null=True, blank=True)
    comment = models.TextField('комментарий', blank=True)

    class Meta:
        verbose_name = 'доставка'
        verbose_name_plural = 'доставки'

    def __str__(self):
        return self.address


class Order(models.Model):
    """Заказ на торт."""

    client = models.OneToOneField(Client, verbose_name='клиент', on_delete=models.PROTECT)
    cake = models.OneToOneField(Cake, verbose_name='торт', on_delete=models.PROTECT)
    price = models.FloatField('стоимость')
    delivery = models.OneToOneField(Delivery, verbose_name='доставка', on_delete=models.PROTECT)
    comment = models.TextField('комментарий', blank=True)

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    def __str__(self):
        return f'Цена: {self.price} рублей. Телефон: {self.client}'

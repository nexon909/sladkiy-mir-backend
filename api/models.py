from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название категории")
    slug = models.SlugField(unique=True, verbose_name="Слаг (cakes, bakery и т.д.)")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name="Категория"
    )
    name = models.CharField(max_length=255, verbose_name="Название товара")
    price = models.DecimalField(max_digits=12, decimal_places=0, verbose_name="Цена (сум)")
    rating = models.FloatField(default=5.0, verbose_name="Рейтинг")
    weight = models.CharField(max_length=50, verbose_name="Вес/Объем (например: 1.5 кг)")
    description = models.TextField(verbose_name="Описание")
    image = models.ImageField(upload_to='products/', max_length=500, verbose_name="Изображение товара")
    is_available = models.BooleanField(default=True, verbose_name="В наличии")

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return f"{self.name} — {self.price} сум"


class Order(models.Model):
    STATUS_CHOICES = [
        ('NEW', 'Новый'),
        ('PROCESSING', 'Готовится'),
        ('DELIVERING', 'В пути'),
        ('COMPLETED', 'Выполнен'),
        ('CANCELLED', 'Отменен'),
    ]

    SLOT_CHOICES = [
        ('10:00 - 12:00', '10:00 - 12:00 (Утро)'),
        ('12:00 - 15:00', '12:00 - 15:00 (Обед)'),
        ('15:00 - 18:00', '15:00 - 18:00 (День)'),
        ('18:00 - 21:00', '18:00 - 21:00 (Вечер)'),
    ]

    customer_name = models.CharField(max_length=100, verbose_name="Имя клиента")
    phone = models.CharField(max_length=30, verbose_name="Телефон")
    telegram = models.CharField(max_length=100, blank=True, null=True, verbose_name="Telegram юзернейм")
    address = models.CharField(max_length=255, verbose_name="Адрес / Ориентир")

    # Поля для даты и временного слота доставки
    delivery_date = models.DateField(blank=True, null=True, verbose_name="Дата доставки")
    delivery_slot = models.CharField(
        max_length=30,
        choices=SLOT_CHOICES,
        default='12:00 - 15:00',
        verbose_name="Слот времени"
    )

    lat = models.FloatField(blank=True, null=True, verbose_name="Широта (Lat)")
    lng = models.FloatField(blank=True, null=True, verbose_name="Долгота (Lng)")
    notes = models.TextField(blank=True, null=True, verbose_name="Комментарий к заказу")
    total_amount = models.DecimalField(max_digits=12, decimal_places=0, verbose_name="Общая сумма")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='NEW', verbose_name="Статус")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f"Заказ №{self.id} — {self.customer_name} ({self.total_amount} сум)"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product_name = models.CharField(max_length=255, verbose_name="Товар")
    price = models.DecimalField(max_digits=12, decimal_places=0, verbose_name="Цена за ед.")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")

    def __str__(self):
        return f"{self.product_name} x {self.quantity}"
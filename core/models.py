from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


def validate_file_size(file):
    """Ограничение размера файла (5 МБ)"""
    max_size = 5 * 1024 * 1024  # 5 МБ
    if file.size > max_size:
        raise ValidationError("Размер файла не должен превышать 5 МБ.")


def create_unique_slug(instance, value):
    base_slug = slugify(value, allow_unicode=True) or "item"
    slug = base_slug
    number = 2

    queryset = instance.__class__.objects.all()

    if instance.pk:
        queryset = queryset.exclude(pk=instance.pk)

    while queryset.filter(slug=slug).exists():
        slug = f"{base_slug}-{number}"
        number += 1

    return slug


class Category(models.Model):
    KIND_CHOICES = (
        ("gazebo", "Беседки"),
        ("enclosure", "Вольеры"),
    )

    name = models.CharField("Название", max_length=150)
    slug = models.SlugField(
        "Адрес страницы",
        max_length=170,
        unique=True,
        blank=True,
        allow_unicode=True,
    )
    kind = models.CharField(
        "Тип продукции",
        max_length=20,
        choices=KIND_CHOICES,
    )
    description = models.TextField("Описание", blank=True)
    is_active = models.BooleanField("Активна", default=True)
    sort_order = models.PositiveIntegerField(
        "Порядок сортировки",
        default=0,
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ("sort_order", "name")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = create_unique_slug(self, self.name)

        super().save(*args, **kwargs)


class Product(models.Model):
    KIND_CHOICES = (
        ("gazebo", "Беседка"),
        ("enclosure", "Вольер"),
    )

    SEASON_CHOICES = (
        ("summer", "Летняя"),
        ("all_season", "Всесезонная"),
        ("winter", "Зимняя"),
    )

    category = models.ForeignKey(
        Category,
        verbose_name="Категория",
        related_name="products",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    kind = models.CharField(
        "Тип продукции",
        max_length=20,
        choices=KIND_CHOICES,
        db_index=True,
    )
    title = models.CharField("Название", max_length=200)
    slug = models.SlugField(
        "Адрес страницы",
        max_length=220,
        unique=True,
        blank=True,
        allow_unicode=True,
    )
    article = models.CharField(
        "Артикул",
        max_length=100,
        blank=True,
    )

    short_description = models.CharField(
        "Краткое описание",
        max_length=500,
        blank=True,
    )
    description = models.TextField("Полное описание", blank=True)
    equipment = models.TextField("Комплектация", blank=True)
    options = models.TextField("Дополнительные опции", blank=True)

    price = models.DecimalField(
        "Цена",
        max_digits=12,
        decimal_places=2,
        default=0,
    )
    old_price = models.DecimalField(
        "Старая цена",
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
    )

    dimensions = models.CharField(
        "Размеры",
        max_length=150,
        blank=True,
    )
    area = models.DecimalField(
        "Площадь, м²",
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
    )

    product_type = models.CharField(
        "Тип конструкции",
        max_length=150,
        blank=True,
    )
    shape = models.CharField("Форма", max_length=150, blank=True)
    frame_material = models.CharField(
        "Материал каркаса",
        max_length=200,
        blank=True,
    )
    wall_material = models.CharField(
        "Материал стен",
        max_length=200,
        blank=True,
    )
    floor_material = models.CharField(
        "Материал пола",
        max_length=200,
        blank=True,
    )
    roof_type = models.CharField(
        "Тип крыши",
        max_length=150,
        blank=True,
    )
    roofing_material = models.CharField(
        "Кровельный материал",
        max_length=200,
        blank=True,
    )
    foundation_type = models.CharField(
        "Тип фундамента",
        max_length=200,
        blank=True,
    )
    insulation_type = models.CharField(
        "Утепление",
        max_length=200,
        blank=True,
    )
    colors = models.CharField(
        "Доступные цвета",
        max_length=500,
        blank=True,
    )

    season = models.CharField(
        "Сезонность",
        max_length=20,
        choices=SEASON_CHOICES,
        default="summer",
    )

    has_grill = models.BooleanField(
        "Есть мангальная зона",
        default=False,
    )
    has_glazing = models.BooleanField(
        "Есть остекление",
        default=False,
    )
    has_booth = models.BooleanField(
        "Есть будка",
        default=False,
    )
    has_winter_room = models.BooleanField(
        "Есть зимник",
        default=False,
    )

    production_days = models.PositiveIntegerField(
        "Срок изготовления, дней",
        default=10,
    )
    warranty_months = models.PositiveIntegerField(
        "Гарантия, месяцев",
        default=12,
    )

    is_available = models.BooleanField(
        "Доступна для заказа",
        default=True,
        db_index=True,
    )
    is_popular = models.BooleanField(
        "Популярное",
        default=False,
        db_index=True,
    )
    is_new = models.BooleanField("Новинка", default=False)
    views_count = models.PositiveIntegerField(
        "Количество просмотров",
        default=0,
    )
    sort_order = models.PositiveIntegerField(
        "Порядок сортировки",
        default=0,
    )

    created_at = models.DateTimeField(
        "Добавлено",
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        "Изменено",
        auto_now=True,
    )

    class Meta:
        verbose_name = "Модель"
        verbose_name_plural = "Модели"
        ordering = ("sort_order", "-created_at")

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = create_unique_slug(self, self.title)

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            "product_detail",
            kwargs={"slug": self.slug},
        )

    @property
    def main_image(self):
        images = list(self.images.all())

        if not images:
            return None

        for image in images:
            if image.is_main:
                return image

        return images[0]

    @property
    def discount(self):
        if (
            self.old_price
            and self.old_price > self.price
            and self.old_price > 0
        ):
            value = (
                (self.old_price - self.price)
                / self.old_price
                * 100
            )
            return int(value)

        return 0


class ProductVariant(models.Model):
    product = models.ForeignKey(
        Product,
        verbose_name="Модель",
        related_name="variants",
        on_delete=models.CASCADE,
    )
    dimensions = models.CharField(
        "Размеры",
        max_length=150,
    )
    price = models.DecimalField(
        "Цена",
        max_digits=12,
        decimal_places=2,
    )
    old_price = models.DecimalField(
        "Старая цена",
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
    )
    description = models.CharField(
        "Комментарий",
        max_length=300,
        blank=True,
    )
    is_default = models.BooleanField(
        "Основной вариант",
        default=False,
    )
    sort_order = models.PositiveIntegerField(
        "Порядок сортировки",
        default=0,
    )

    class Meta:
        verbose_name = "Размер и цена"
        verbose_name_plural = "Размеры и цены"
        ordering = ("sort_order", "price")

    def __str__(self):
        return f"{self.product.title}: {self.dimensions}"


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        verbose_name="Модель",
        related_name="images",
        on_delete=models.CASCADE,
    )
    image = models.ImageField(
        "Фотография",
        upload_to="products/%Y/%m/",
    )
    alt = models.CharField(
        "Описание фотографии",
        max_length=250,
        blank=True,
    )
    is_main = models.BooleanField(
        "Главная фотография",
        default=False,
    )
    sort_order = models.PositiveIntegerField(
        "Порядок сортировки",
        default=0,
    )

    class Meta:
        verbose_name = "Фотография модели"
        verbose_name_plural = "Фотографии модели"
        ordering = ("-is_main", "sort_order", "id")

    def __str__(self):
        return f"Фото: {self.product.title}"


class Project(models.Model):
    PROJECT_TYPE_CHOICES = (
        ("gazebo", "Беседка"),
        ("winter_gazebo", "Зимняя беседка"),
        ("grill_gazebo", "Беседка с мангалом"),
        ("enclosure", "Вольер"),
        ("winter_enclosure", "Зимний вольер"),
    )

    title = models.CharField("Название", max_length=200)
    project_type = models.CharField(
        "Тип проекта",
        max_length=30,
        choices=PROJECT_TYPE_CHOICES,
    )
    description = models.TextField("Описание", blank=True)
    dimensions = models.CharField(
        "Размеры",
        max_length=150,
        blank=True,
    )
    materials = models.CharField(
        "Материалы",
        max_length=500,
        blank=True,
    )
    installation_location = models.CharField(
        "Место установки",
        max_length=250,
        blank=True,
    )
    completion_days = models.PositiveIntegerField(
        "Срок выполнения, дней",
        default=10,
    )
    approximate_price = models.DecimalField(
        "Примерная стоимость",
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
    )
    image_before = models.ImageField(
        "Фотография до",
        upload_to="projects/before/%Y/%m/",
        null=True,
        blank=True,
    )
    image_after = models.ImageField(
        "Фотография после",
        upload_to="projects/after/%Y/%m/",
        null=True,
        blank=True,
    )
    is_published = models.BooleanField(
        "Опубликован",
        default=True,
        db_index=True,
    )
    sort_order = models.PositiveIntegerField(
        "Порядок сортировки",
        default=0,
    )
    created_at = models.DateTimeField(
        "Добавлен",
        auto_now_add=True,
    )

    class Meta:
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"
        ordering = ("sort_order", "-created_at")

    def __str__(self):
        return self.title


class Review(models.Model):
    name = models.CharField("Имя клиента", max_length=150)
    text = models.TextField("Текст отзыва")
    rating = models.PositiveSmallIntegerField(
        "Оценка",
        default=5,
    )
    product = models.ForeignKey(
        Product,
        verbose_name="Модель",
        related_name="reviews",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    is_published = models.BooleanField(
        "Опубликован",
        default=True,
        db_index=True,
    )
    created_at = models.DateTimeField(
        "Добавлен",
        auto_now_add=True,
    )

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.name}: {self.rating}/5"


class GalleryImage(models.Model):
    title = models.CharField(
        "Название",
        max_length=200,
        blank=True,
    )
    image = models.ImageField(
        "Фотография",
        upload_to="gallery/%Y/%m/",
    )
    description = models.CharField(
        "Описание",
        max_length=300,
        blank=True,
    )
    is_published = models.BooleanField(
        "Опубликована",
        default=True,
    )
    sort_order = models.PositiveIntegerField(
        "Порядок сортировки",
        default=0,
    )

    class Meta:
        verbose_name = "Фотография галереи"
        verbose_name_plural = "Галерея"
        ordering = ("sort_order", "id")

    def __str__(self):
        return self.title or f"Фотография №{self.pk}"


class Application(models.Model):
    PROJECT_TYPE_CHOICES = (
        ("gazebo", "Беседка"),
        ("enclosure", "Вольер"),
        ("winter_enclosure", "Зимний вольер"),
        ("other", "Другое"),
    )

    STATUS_CHOICES = (
        ("new", "Новая"),
        ("processing", "В работе"),
        ("completed", "Завершена"),
        ("cancelled", "Отменена"),
    )

    name = models.CharField("Имя", max_length=150)
    phone = models.CharField("Телефон", max_length=50)
    email = models.EmailField("Электронная почта", blank=True)
    project_type = models.CharField(
        "Тип проекта",
        max_length=30,
        choices=PROJECT_TYPE_CHOICES,
        default="gazebo",
    )
    selected_model = models.CharField(
        "Выбранная модель",
        max_length=200,
        blank=True,
    )
    dimensions = models.CharField(
        "Размеры",
        max_length=150,
        blank=True,
    )
    material = models.CharField(
        "Материал",
        max_length=250,
        blank=True,
    )
    roof_type = models.CharField(
        "Тип крыши",
        max_length=200,
        blank=True,
    )
    options = models.TextField(
        "Дополнительные опции",
        blank=True,
    )
    address = models.CharField(
        "Адрес доставки и установки",
        max_length=300,
        blank=True,
    )
    comment = models.TextField("Комментарий", blank=True)
    attachment = models.FileField(
        "Прикреплённый файл",
        upload_to="applications/%Y/%m/",
        null=True,
        blank=True,
        validators=[
            FileExtensionValidator(
                ["jpg", "jpeg", "png", "webp", "pdf", "doc", "docx"]
            ),
            validate_file_size,
        ],
    )
    status = models.CharField(
        "Статус",
        max_length=20,
        choices=STATUS_CHOICES,
        default="new",
        db_index=True,
    )
    created_at = models.DateTimeField(
        "Дата отправки",
        auto_now_add=True,
    )

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.name} — {self.phone}"
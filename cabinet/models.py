from django.conf import settings
from django.db import models
from django.urls import reverse

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Review(models.Model):
    RATING_CHOICES = [
        (5, "5 — отлично"),
        (4, "4 — хорошо"),
        (3, "3 — удовлетворительно"),
        (2, "2 — плохо"),
        (1, "1 — очень плохо"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Клиент",
    )

    text = models.TextField(
        verbose_name="Текст отзыва",
        max_length=2000,
    )

    rating = models.PositiveSmallIntegerField(
        verbose_name="Оценка",
        choices=RATING_CHOICES,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5),
        ],
    )

    is_published = models.BooleanField(
        default=False,
        verbose_name="Опубликован",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

    def __str__(self):
        return f"{self.user} — {self.rating}/5"
    
class Application(models.Model):
    class ProjectType(models.TextChoices):
        GAZEBO = "gazebo", "Беседка"
        AVIARY = "aviary", "Вольер"
        WINTER_AVIARY = "winter_aviary", "Зимний вольер"
        CANOPY = "canopy", "Навес"
        OTHER = "other", "Индивидуальный проект"

    class Status(models.TextChoices):
        NEW = "new", "Новая"
        ACCEPTED = "accepted", "Принята"
        IN_PROGRESS = "in_progress", "В работе"
        COMPLETED = "completed", "Завершена"
        CANCELLED = "cancelled", "Отменена"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="client_applications",
        verbose_name="Клиент",
    )

    project_type = models.CharField(
        max_length=30,
        choices=ProjectType.choices,
        verbose_name="Тип проекта",
    )

    name = models.CharField(
        max_length=150,
        verbose_name="Имя",
    )

    phone = models.CharField(
        max_length=30,
        verbose_name="Телефон",
    )

    description = models.TextField(
        blank=True,
        verbose_name="Описание и пожелания",
    )

    status = models.CharField(
        max_length=30,
        choices=Status.choices,
        default=Status.NEW,
        verbose_name="Статус",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата изменения",
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"

    def __str__(self):
        return f"Заявка №{self.pk}: {self.get_project_type_display()}"

    def get_absolute_url(self):
        return reverse(
            "cabinet:application_detail",
            kwargs={"pk": self.pk},
        )
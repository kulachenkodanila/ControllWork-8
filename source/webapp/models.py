from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.
CHOICES = [('food', 'Еда'), ('toys', 'Игрушки'),
           ('tools', 'Инструменты')]


class Product(models.Model):
    name = models.CharField(max_length=50, verbose_name="Наименование")
    category = models.CharField(max_length=50, choices=CHOICES, default=CHOICES[0][0],
                                verbose_name='Категории')
    description = models.TextField(max_length=5000, null=True, blank=True, verbose_name="Описание")
    image = models.ImageField(upload_to="images", null=True, blank=True, verbose_name="Картинка")

    def __str__(self):
        return f"{self.id}. {self.name}: {self.category}"

    class Meta:
        db_table = "products"
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"




class Review(models.Model):
    author = models.ForeignKey(get_user_model(), related_name="products", verbose_name="Автор",
                               on_delete=models.CASCADE)
    product = models.ForeignKey("webapp.Product", on_delete=models.CASCADE, related_name="products",
                                verbose_name="Продукт")
    text = models.TextField(max_length=5000, verbose_name="Текст")
    mark = models.IntegerField(verbose_name='Оценка')
    moderated = models.BooleanField(default=False, verbose_name="Модерированный")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")

    def __str__(self):
        return f"{self.id}. {self.author}. {self.product}. {self.text}. {self.mark}. {self.moderated}"

    class Meta:
        db_table = "reviews"
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

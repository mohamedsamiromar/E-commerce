from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Item(models.Model):
    merchant = models.ForeignKey(
        'merchants.MerchantProfile',
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='products',
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, blank=True, null=True, related_name='items'
    )
    title = models.CharField(max_length=100)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    image = models.ImageField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    in_stock = models.BooleanField(default=True)
    stock_qty = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.title

    @property
    def has_discount(self):
        return self.discount_price is not None

    @property
    def final_price(self):
        return self.discount_price if self.has_discount else self.price

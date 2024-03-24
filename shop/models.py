import random
import string

from django.db import models
from django.urls import reverse
from django.utils.text import slugify


def rand_slug():
    """
    Generates a random slug consisting of lowercase letters and digits.

    Returns:
        str: A random slug.

    Example:
          >>> rand_slug()
          'abc123'

    """
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(3))


class Category(models.Model):
    """
    A model representing a category.

    """
    name = models.CharField('Category', max_length=250, db_index=True)
    parent = models.ForeignKey('Parent category',
                               'self', on_delete=models.CASCADE, related_name='children', blank=True, null=True
                               )
    slug = models.SlugField('URL', max_length=250, unique=True, null=False, editable=True)
    created_at = models.DateTimeField('Created date', auto_now_add=True)

    class Meta:
        unique_together = ('slug', 'parent')
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        """
        Returns a string representation object.

        """
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return '> '.join(full_path[::-1])

    def save(self, *args, **kwargs):
        """
        Save the current instance to the database.

        """
        if not self.slug:
            self.slug = slugify(rand_slug() + 'pickBetter' + self.name)
        super(Category, self).save(*args, **kwargs)

    # def get_absolute_url(self):
    #     return reverse('model_detail', kwargs={'pk': self.pk})


class Product(models.Model):
    """
    A model representing a product.

    """
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    title = models.CharField('Title', max_length=250)
    brand = models.CharField('Brand', max_length=250)
    description = models.TextField('Description', blank=True)
    slug = models.SlugField('URL', max_length=250)
    price = models.DecimalField('Price', max_digits=7, decimal_places=2, default=99.99)
    image = models.ImageField("Image", upload_to='products/products/%Y/%m/%d')
    available = models.BooleanField('Available', default=True)
    created_at = models.DateTimeField('Created date', auto_now_add=True)
    uploaded_at = models.DateTimeField("Uploaded date", auto_now=True)

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    # def get_absolute_url(self):
    #     return reverse('model_detail', kwargs={'pk': self.pk})


class ProductManager(models.Manager):
    def get_queryset(self):
        """
        Returns a queryset of products that are available.

        Returns:
            QuerySet: A queryset of products that are available

        """
        return super(ProductManager, self).get_queryset().filter(available=True)


class ProductProxy(Product):

    objects = ProductManager()

    class Meta:
        proxy = True

from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=250, db_index=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='children', blank=True, null=True)

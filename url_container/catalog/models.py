from django.db import models
from user.models import CustomUser


class Collection(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)


    def __str__(self):
        return f"{self.name}"



class Container(models.Model):
    title = models.TextField()
    description = models.TextField()
    url = models.TextField()
    image = models.ImageField(upload_to='product_images/')
    url_type = models.CharField(max_length=100)
    collection = models.ManyToManyField(Collection, null=True, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    changed_at = models.DateTimeField(auto_now_add=True)

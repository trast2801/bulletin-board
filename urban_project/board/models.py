from django.db import models
from django.contrib.auth.models import User


class Advertisement(models.Model):
    '''описание модели таблицы  аdvertisement'''
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='advertisements', null=True, blank=True)

    def get_image_path(self):
        return self.image.path

    def get_image_url(self):
        return self.image.url

    def get_image_name(self):
        return self.image.name

    def get_image_full_path(self):
        return self.get_image_path()

    def __str__(self):
        return self.title


class Comment(models.Model):
    '''описание модели таблицы comment'''
    advertisement = models.ForeignKey(Advertisement, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author} on {self.advertisement}'

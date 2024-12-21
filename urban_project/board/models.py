from django.db import models
from django.contrib.auth.models import User
from vote.managers import VotableManager
from vote.models import VoteModel




class Advertisement( VoteModel):
    '''
       описание модели таблицы  аdvertisement,
       Подключена библиотека django_vote для оценки рекламмных сообщений
    '''
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='advertisements', null=True, blank=True)
    objects = VotableManager()

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

class Stat(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    advertisement_count = models.IntegerField(default=0)

    def __str__(self):
        """Возвращает строковое представление профиля пользователя."""
        return self.user.username

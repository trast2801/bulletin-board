from django.contrib.auth import user_logged_in
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from vote.models import Vote

from .models import Advertisement, Stat


@receiver(post_save, sender=Advertisement)
def update_advertisement_count_add(sender, instance, created, **kwargs):
    """
    Сигнал для обновления количества созданных объявлений.
    """
    if created:
        profile, _ = Stat.objects.get_or_create(user=instance.author)
        profile.advertisement_count += 1

        profile.save()


@receiver(post_delete, sender=Advertisement)
def update_advertisement_count_del(sender, instance, **kwargs):
    """
    Сигнал для обновления количества удаленных объявлений. C защитой от минусов
    """
    profile, _ = Stat.objects.get_or_create(user=instance.author)
    if profile.advertisement_count > 0:
        profile.advertisement_count -= 1
    else:
        profile.advertisement_count = 0
    profile.save()

from django.db.models.signals import post_delete
from django.dispatch import receiver

from main.models import Rented, Item


@receiver(post_delete, sender=Rented)
def update_stock(sender, instance, *args, **kwargs):
    obj = Item.objects.get(pk=instance.item.pk)
    obj.stock += 1
    obj.save()

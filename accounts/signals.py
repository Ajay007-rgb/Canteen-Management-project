from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile


@receiver(post_save, sender=User)
def create_or_update_profile(sender, instance, created, **kwargs):
    """Automatically create a Profile whenever a User is created, and
    keep is_admin in sync with is_staff."""
    if created:
        Profile.objects.create(user=instance, is_admin=instance.is_staff)
    else:
        Profile.objects.filter(user=instance).update(is_admin=instance.is_staff)

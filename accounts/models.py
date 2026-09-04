from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    """Extra information attached to every Django User.

    Role is kept simple on purpose: `is_admin` mirrors `User.is_staff`
    but is exposed here so templates/views can check a single flag
    (`profile.is_admin`) without caring about Django's own permission
    system. Real admin authorization still relies on `is_staff`.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} profile"

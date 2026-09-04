from django.contrib.auth.decorators import user_passes_test

# A normal student must never reach any dashboard view. is_staff is Django's
# built-in, battle-tested permission flag, so we gate every dashboard view on
# it rather than inventing our own check.
admin_required = user_passes_test(lambda u: u.is_authenticated and u.is_staff, login_url='accounts:login')

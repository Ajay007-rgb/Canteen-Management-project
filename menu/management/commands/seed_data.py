from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from menu.models import Category, FoodItem


class Command(BaseCommand):
    help = 'Seed the database with sample categories, food items, and an admin user.'

    def handle(self, *args, **options):
        categories = ['Breakfast', 'Lunch', 'Snacks', 'Fast Food', 'Beverages']
        cat_objs = {}
        for name in categories:
            obj, _ = Category.objects.get_or_create(name=name)
            cat_objs[name] = obj
        self.stdout.write(self.style.SUCCESS(f'Categories ready: {", ".join(categories)}'))

        sample_items = [
            ('Samosa', 'Crispy fried pastry with spiced potato filling', 'Snacks', 15),
            ('Burger', 'Classic veg burger with lettuce, tomato and cheese', 'Fast Food', 60),
            ('Veg Sandwich', 'Grilled sandwich with fresh vegetables', 'Snacks', 50),
            ('Masala Dosa', 'South Indian crepe with spiced potato filling', 'Breakfast', 70),
            ('Cold Drink', 'Chilled aerated soft drink', 'Beverages', 30),
            ('Tea', 'Hot Indian masala chai', 'Beverages', 15),
            ('Veg Thali', 'Full meal with rice, dal, sabzi and roti', 'Lunch', 90),
            ('Paneer Roll', 'Paneer tikka wrapped in a soft roti', 'Fast Food', 65),
            ('Idli Sambhar', 'Steamed rice cakes with lentil sambhar', 'Breakfast', 40),
            ('Cold Coffee', 'Chilled sweetened coffee with ice cream', 'Beverages', 45),
        ]
        for name, desc, cat, price in sample_items:
            FoodItem.objects.get_or_create(
                name=name,
                defaults={'description': desc, 'category': cat_objs[cat], 'price': price, 'is_available': True}
            )
        self.stdout.write(self.style.SUCCESS(f'{len(sample_items)} sample food items ready.'))

        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@canteen.local', 'AdminPass123')
            self.stdout.write(self.style.SUCCESS('Superuser "admin" created (username: admin / password: AdminPass123). Change this password immediately.'))
        else:
            self.stdout.write('Superuser "admin" already exists, skipping.')

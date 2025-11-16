from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from faker import Faker
import random


class Command(BaseCommand):
    help = 'Generate fake users in bulk (default: 10000)'

    def add_arguments(self, parser):
        parser.add_argument('--count', type=int, default=10000, help='Total number of users to create')
        parser.add_argument('--batch-size', type=int, default=1000, help='Batch size for bulk_create')
        parser.add_argument('--password', type=str, default='12345', help='Plain password to set for all users')
        parser.add_argument('--seed', type=int, default=None, help='Random seed for reproducibility')

    def handle(self, *args, **options):
        count = options['count']
        batch_size = options['batch_size']
        raw_password = options['password']
        seed = options.get('seed')

        if seed is not None:
            random.seed(seed)

        fake = Faker()
        User = get_user_model()

        departments = ["IT", "HR", "Sales", "Finance"]
        roles = [choice[0] for choice in getattr(User, 'ROLE_CHOICES', [])] or ["admin", "manager", "employee"]

        # Pre-hash password once for efficiency
        hashed_password = make_password(raw_password)

        users_to_create = []
        created = 0

        self.stdout.write(self.style.NOTICE(f'Starting creation of {count} users (batch_size={batch_size})'))

        for i in range(count):
            email = fake.unique.email()
            first_name = fake.first_name()
            last_name = fake.last_name()
            username = fake.user_name()
            phone = fake.phone_number()
            city = fake.city()
            country = fake.country()
            department = random.choice(departments)
            role = random.choice(roles)
            birth_year = random.randint(1975, 2005)
            birth_date = fake.date_of_birth(minimum_age=0, maximum_age=100)
            # ensure year range
            birth_date = birth_date.replace(year=random.randint(1975, 2005))

            user = User(
                email=email,
                username=username,
                first_name=first_name,
                last_name=last_name,
                phone=phone,
                city=city,
                country=country,
                department=department,
                role=role,
                birth_date=birth_date,
                salary=random.randint(300, 10000),
                is_active=True,
                is_staff=False,
                date_joined=timezone.now(),
                password=hashed_password,
            )

            users_to_create.append(user)

            if len(users_to_create) >= batch_size:
                User.objects.bulk_create(users_to_create, batch_size)
                created += len(users_to_create)
                self.stdout.write(self.style.SUCCESS(f'Created {created}/{count} users'))
                users_to_create = []

        # final batch
        if users_to_create:
            User.objects.bulk_create(users_to_create, batch_size)
            created += len(users_to_create)
            self.stdout.write(self.style.SUCCESS(f'Created {created}/{count} users'))

        self.stdout.write(self.style.SUCCESS(f'Done — total users created: {created}'))

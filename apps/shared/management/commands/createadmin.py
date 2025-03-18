import os
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from environs import Env

env = Env()
env.read_env('envs/.env')


class Command(BaseCommand):
    help = "Creates a superuser if it doesn't exist using .env variables"

    def handle(self, *args, **options):
        User = get_user_model()

        username = env.str("DJANGO_SUPERUSER_USERNAME", "admin")
        email = env.str("DJANGO_SUPERUSER_EMAIL", "admin@example.com")
        password = env.str("DJANGO_SUPERUSER_PASSWORD", "admin123")

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f"Superuser '{username}' created successfully."))
        else:
            self.stdout.write(self.style.SUCCESS(f"Superuser '{username}' already exists."))

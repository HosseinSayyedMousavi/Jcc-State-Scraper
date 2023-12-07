
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from decouple import config
class Command(BaseCommand):
    help = 'Create a superuser if it does not exist'

    def handle(self, *args, **options):
        if not User.objects.filter(username=config('ADMIN_SUPER_USER')).exists():
            User.objects.create_superuser(config("ADMIN_SUPER_USER"),config("ADMIN_EMAIL") ,config("ADMIN_PASSWORD"))
            self.stdout.write(self.style.SUCCESS('Superuser created successfully'))
        else:
            self.stdout.write(self.style.SUCCESS('Superuser already exists'))

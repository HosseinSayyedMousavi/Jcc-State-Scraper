from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from decouple import config
from apscheduler.schedulers.background import BackgroundScheduler
from ...scrape import scrape_ojcc
class Command(BaseCommand):
    help = 'run the main scraper'
    def handle(self, *args, **options):
        scheduler = BackgroundScheduler()
        scheduler.add_job(
            func = scrape_ojcc,
            trigger = "interval",
            minutes = config("SCHEDULER_INTERVAL",cast=int)
        )
        scheduler.start()
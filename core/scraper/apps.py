from django.apps import AppConfig

import threading


class ScraperConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'scraper'
    def ready(self):
        from .functions import start_scraper
        threading.Thread(target=start_scraper).start()

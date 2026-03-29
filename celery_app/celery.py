import os
from celery import Celery

# ============================================================
# CELERY CONFIGURATION
# ============================================================
# Why: Set Django settings module for Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Why: Create Celery app instance
app = Celery('nexamart')

# Why: Load config from Django settings
# All celery settings start with CELERY_ prefix
app.config_from_object('django.conf:settings', namespace='CELERY')

# Why: Auto discover tasks from all installed apps
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
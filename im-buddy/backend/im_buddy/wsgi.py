"""
WSGI config for im_buddy project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'im_buddy.settings')

application = get_wsgi_application() 
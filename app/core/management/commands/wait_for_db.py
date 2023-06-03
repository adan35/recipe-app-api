"""
Django command for wait for the database to be avaliable
"""
from typing import Any
from django.core.management import BaseCommand

class Command(BaseCommand):
  """Django command to wait for database"""

  def handle(self, *args, **options):
    pass
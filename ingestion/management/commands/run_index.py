import os
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'List all files in the provided directory path'

    def add_arguments(self, parser):
        parser.add_argument('path', type=str, help='The directory path')

    def handle(self, *args, **kwargs):
        directory_path = kwargs['path']

        if not os.path.exists(directory_path):
            self.stdout.write(
                self.style.ERROR(f"The path {directory_path} does not exist."))
            return

        if not os.path.isdir(directory_path):
            self.stdout.write(
                self.style.ERROR(f"The path {directory_path} is not a directory."))
            return

        files = os.listdir(directory_path)
        if not files:
            self.stdout.write(f"The directory {directory_path} is empty.")
        else:
            self.stdout.write(f"Files in {directory_path}:")
            for file in files:
                self.stdout.write(f"- {file}")

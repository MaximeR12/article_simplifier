import os
from django.core.management.base import BaseCommand
from dotenv import set_key

class Command(BaseCommand):
    help = 'Change an environment variable in the project'

    def add_arguments(self, parser):
        parser.add_argument('variable_name', type=str, help='Name of the environment variable')
        parser.add_argument('new_value', type=str, help='New value for the environment variable')

    def handle(self, *args, **options):
        variable_name = options['variable_name']
        new_value = options['new_value']

        # Obtenez le chemin absolu du fichier .env
        env_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), '..', '.env')

        set_key(env_file_path, variable_name, new_value)

        self.stdout.write(self.style.SUCCESS(f'Successfully changed {variable_name} to {new_value}'))

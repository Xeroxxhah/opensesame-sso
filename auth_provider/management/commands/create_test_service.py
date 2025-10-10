from django.core.management.base import BaseCommand
from auth_provider.models import ServiceProvider
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = 'Creates a test service provider for development'

    def add_arguments(self, parser):
        parser.add_argument(
            '--name',
            type=str,
            default='Test Service',
            help='Service provider name'
        )
        parser.add_argument(
            '--redirect-url',
            type=str,
            default='http://localhost:8000/web.sso/success/',
            help='Redirect URL after authentication'
        )

    def handle(self, *args, **options):
        name = options['name']
        redirect_url = options['redirect_url']

        # Check if service already exists
        existing = ServiceProvider.objects.filter(service_name=name).first()
        if existing:
            self.stdout.write(
                self.style.WARNING(f'Service "{name}" already exists!')
            )
            self.stdout.write(f'Service ID: {existing.service_id}')
            self.stdout.write(f'Redirect URL: {existing.redirect_url}')
            return

        # Create new service provider
        service = ServiceProvider.objects.create(
            service_name=name,
            redirect_url=redirect_url,
            claims_required={}
        )

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created service provider "{name}"')
        )
        self.stdout.write(f'\nService Details:')
        self.stdout.write(f'  Name: {service.service_name}')
        self.stdout.write(f'  Service ID: {service.service_id}')
        self.stdout.write(f'  Redirect URL: {service.redirect_url}')
        self.stdout.write(f'  Service Secret: {service.service_secret[:20]}...')

        self.stdout.write(
            self.style.SUCCESS('\n\nUse this URL to test:')
        )
        self.stdout.write(
            f'http://127.0.0.1:8000/web.sso/login/?service_id={service.service_id}'
        )
        self.stdout.write(
            f'http://127.0.0.1:8000/web.sso/pla-login/?service_id={service.service_id}'
        )

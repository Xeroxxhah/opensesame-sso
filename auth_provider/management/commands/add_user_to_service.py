from django.core.management.base import BaseCommand
from auth_provider.models import ServiceProvider, ServiceProviderUser
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = 'Adds a user to a service provider'

    def add_arguments(self, parser):
        parser.add_argument(
            '--email',
            type=str,
            required=True,
            help='User email address'
        )
        parser.add_argument(
            '--service-id',
            type=str,
            help='Service provider ID (optional - uses first service if not provided)'
        )

    def handle(self, *args, **options):
        email = options['email']
        service_id = options.get('service_id')

        User = get_user_model()

        # Get user
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'User with email "{email}" does not exist!')
            )
            self.stdout.write('\nCreate a user first using:')
            self.stdout.write('  python manage.py createsuperuser')
            return

        # Get service provider
        if service_id:
            try:
                service = ServiceProvider.objects.get(service_id=service_id)
            except ServiceProvider.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'Service with ID "{service_id}" does not exist!')
                )
                return
        else:
            service = ServiceProvider.objects.first()
            if not service:
                self.stdout.write(
                    self.style.ERROR('No service providers found!')
                )
                self.stdout.write('\nCreate a service provider first using:')
                self.stdout.write('  python manage.py create_test_service')
                return

        # Check if already exists
        if ServiceProviderUser.objects.filter(user=user, serviceprovider=service).exists():
            self.stdout.write(
                self.style.WARNING(f'User "{email}" is already registered with service "{service.service_name}"')
            )
            return

        # Create the relationship
        ServiceProviderUser.objects.create(
            user=user,
            serviceprovider=service,
            is_active=True
        )

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully added user "{email}" to service "{service.service_name}"'
            )
        )
        self.stdout.write(f'\nService Details:')
        self.stdout.write(f'  Name: {service.service_name}')
        self.stdout.write(f'  Service ID: {service.service_id}')
        self.stdout.write(f'\nYou can now login at:')
        self.stdout.write(
            f'  http://127.0.0.1:8000/web.sso/login/?service_id={service.service_id}'
        )
        self.stdout.write(
            f'  http://127.0.0.1:8000/web.sso/pla-login/?service_id={service.service_id}'
        )

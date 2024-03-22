from django.contrib.auth.management.commands import createsuperuser

class Command(createsuperuser.Command):
    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument(
            '--name', 
            dest='name', 
            default=None,
            help='Specifies the name for the superuser.',
        )

    def handle(self, *args, **options):
        name = options.get('name')
        if name is None:
            name = input('Name: ')
        options['name'] = name
        super().handle(*args, **options)

import os

from django.core.management.commands import shell
from django.contrib.auth import get_user_model


class Command(shell.Command):
    help = 'Create superuser if it does not exist'

    def handle(self, *args, **options):
        superuser = os.getenv('APP_SUPERUSER') or 'admin'
        superpass = os.getenv('APP_SUPERPASS') or 'admin'

        UserModel = get_user_model()
        if not UserModel.objects.filter(username=superuser).exists():
            self.stdout.write(f'Creating superuser: {superuser}')
            UserModel.objects.create_superuser(  # type: ignore
                superuser,
                email=None,
                password=superpass,
            )
        else:
            self.stdout.write(f'User {superuser} exists')

from django.core.management.base import BaseCommand
from contact.models import Contact, ServiceMessage, ServiceNote

class Command(BaseCommand):
    help = 'Elimina todos los servicios, mensajes y notas existentes'

    def add_arguments(self, parser):
        parser.add_argument(
            '--confirm',
            action='store_true',
            help='Confirmar la eliminación sin preguntar',
        )

    def handle(self, *args, **options):
        if not options['confirm']:
            self.stdout.write(
                self.style.WARNING(
                    '⚠️  ADVERTENCIA: Esto eliminará TODOS los servicios existentes.\n'
                    'Para continuar, ejecuta: python manage.py clear_services --confirm'
                )
            )
            return

        # Contar registros antes de eliminar
        contact_count = Contact.objects.count()
        message_count = ServiceMessage.objects.count()
        note_count = ServiceNote.objects.count()

        # Eliminar todos los datos
        Contact.objects.all().delete()
        ServiceMessage.objects.all().delete()
        ServiceNote.objects.all().delete()

        self.stdout.write(
            self.style.SUCCESS(
                f'✅ Limpieza completada exitosamente:\n'
                f'   • {contact_count} servicios eliminados\n'
                f'   • {message_count} mensajes eliminados\n'
                f'   • {note_count} notas eliminadas\n\n'
                f'📝 Los nuevos servicios ya no incluirán la letra "O" para evitar confusión con el número "0"'
            )
        ) 
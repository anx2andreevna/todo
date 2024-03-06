from django.core.management.base import BaseCommand, CommandError
from todo.models import Task

class Command(BaseCommand):
    help = 'Hiding the specified task'

    def add_arguments(self, parser):
        parser.add_argument('task_ids', nargs='+', type=int)

    def handle(self, *args, **options):
        for task_id in options['task_ids']:
            try:
                task = Task.objects.get(pk=task_id)
            except Task.DoesNotExist:
                raise CommandError('Task "%s" does not exist' % task_id)

            task.is_hidden = True
            task.save()

            self.stdout.write(self.style.SUCCESS('Successfully hide task "%s"' % task_id))
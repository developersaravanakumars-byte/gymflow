from django.core.management.base import BaseCommand
from django.utils import timezone
from members.models import Member


class Command(BaseCommand):
    help = 'Archive members whose membership has expired'

    def handle(self, *args, **kwargs):
        today = timezone.now().date()
        archived = Member.objects.filter(
            membership_expiry__lt=today,
            is_archived=False
        ).update(is_archived=True)
        self.stdout.write(
            self.style.SUCCESS(f'Successfully archived {archived} expired member(s).')
        )

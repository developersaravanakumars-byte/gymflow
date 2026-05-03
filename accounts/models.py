from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = [
        ('owner', 'Owner'),
        ('manager', 'Branch Manager'),
        ('staff', 'Staff'),
        ('trainer', 'Trainer'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='staff')
    branch = models.ForeignKey(
        'branches.Branch',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='staff_members'
    )
    phone = models.CharField(max_length=15, blank=True)

    def is_owner(self):
        return self.role == 'owner'

    def is_manager(self):
        return self.role == 'manager'

    def get_accessible_branches(self):
        from branches.models import Branch
        if self.is_owner():
            return Branch.objects.all()
        return Branch.objects.filter(id=self.branch_id)

    def __str__(self):
        return f'{self.username} ({self.get_role_display()})'

from django.db import models
from branches.models import Branch


class Enquiry(models.Model):
    SOURCE_CHOICES = [
        ('walk_in', 'Walk-in'),
        ('call', 'Phone Call'),
        ('online', 'Online'),
        ('referral', 'Referral'),
        ('other', 'Other'),
    ]
    STATUS_CHOICES = [
        ('new', 'New'),
        ('follow_up', 'Follow-up'),
        ('converted', 'Converted'),
        ('lost', 'Lost'),
    ]

    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='enquiries')
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True)
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES, default='walk_in')
    interests = models.CharField(max_length=255, blank=True, help_text='e.g. Weight loss, Bodybuilding')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    follow_up_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    converted_member = models.OneToOneField(
        'members.Member', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='enquiry'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Enquiries'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} ({self.get_status_display()})'

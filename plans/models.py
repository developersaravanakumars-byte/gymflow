from django.db import models


class Plan(models.Model):
    DURATION_UNIT_CHOICES = [
        ('days', 'Days'),
        ('months', 'Months'),
        ('years', 'Years'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    duration = models.PositiveIntegerField(help_text='Number of days/months/years')
    duration_unit = models.CharField(max_length=10, choices=DURATION_UNIT_CHOICES, default='months')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['price']

    def __str__(self):
        return f'{self.name} — ₹{self.price} / {self.duration} {self.duration_unit}'

    def duration_in_days(self):
        if self.duration_unit == 'days':
            return self.duration
        elif self.duration_unit == 'months':
            return self.duration * 30
        return self.duration * 365

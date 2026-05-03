from django.db import models
from members.models import Member
from plans.models import Plan


class Payment(models.Model):
    STATUS_CHOICES = [
        ('paid', 'Paid'),
        ('pending', 'Pending'),
        ('overdue', 'Overdue'),
    ]
    METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('upi', 'UPI'),
        ('card', 'Card'),
        ('bank', 'Bank Transfer'),
        ('other', 'Other'),
    ]

    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='payments')
    plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True, blank=True)
    receipt_number = models.CharField(max_length=20, unique=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    final_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='paid')
    method = models.CharField(max_length=10, choices=METHOD_CHOICES, default='cash')
    coverage_from = models.DateField()
    coverage_to = models.DateField()
    paid_on = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.member.full_name} — ₹{self.final_amount} ({self.get_status_display()})'

    def save(self, *args, **kwargs):
        if not self.receipt_number:
            last = Payment.objects.order_by('-id').first()
            next_id = (last.id + 1) if last else 1
            self.receipt_number = f'RCP-{next_id:05d}'
        self.final_amount = self.amount - self.discount
        super().save(*args, **kwargs)


class Invoice(models.Model):
    payment = models.OneToOneField(Payment, on_delete=models.CASCADE, related_name='invoice')
    invoice_number = models.CharField(max_length=20, unique=True)
    issued_on = models.DateField(auto_now_add=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-issued_on']

    def __str__(self):
        return f'Invoice #{self.invoice_number}'

    def save(self, *args, **kwargs):
        if not self.invoice_number:
            last = Invoice.objects.order_by('-id').first()
            next_id = (last.id + 1) if last else 1
            self.invoice_number = f'GYM-{next_id:05d}'
        super().save(*args, **kwargs)

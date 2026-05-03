from django.db import models
from branches.models import Branch


class Member(models.Model):
    GENDER_CHOICES = [('M', 'Male'), ('F', 'Female'), ('O', 'Other')]

    # Branch
    branch = models.ForeignKey(Branch, on_delete=models.PROTECT, related_name='members')

    # Unique member ID (e.g. GF-KRM-0001)
    member_id = models.CharField(max_length=20, unique=True, blank=True, editable=False)

    # Personal info
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(blank=True)
    photo = models.ImageField(upload_to='members/', blank=True, null=True)

    # Membership
    membership_start = models.DateField(null=True, blank=True)
    membership_expiry = models.DateField(null=True, blank=True)
    plan = models.ForeignKey(
        'plans.Plan', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='members'
    )

    # Status
    is_archived = models.BooleanField(default=False)
    joined_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['first_name', 'last_name']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def save(self, *args, **kwargs):
        if not self.member_id:
            # Build a 3-letter prefix from branch name (e.g. "Karatumedu" -> "KAR")
            branch_prefix = ''.join(
                c for c in self.branch.name.upper() if c.isalpha()
            )[:3]
            # Find the next sequence number across all members of this branch
            last = Member.objects.filter(
                branch=self.branch
            ).order_by('-id').first()
            next_seq = (last.id + 1) if last else 1
            self.member_id = f'GF-{branch_prefix}-{next_seq:04d}'
        super().save(*args, **kwargs)

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def is_active_member(self):
        from django.utils import timezone
        if self.membership_expiry:
            return self.membership_expiry >= timezone.now().date() and not self.is_archived
        return False

    @property
    def days_until_expiry(self):
        from django.utils import timezone
        if self.membership_expiry:
            delta = self.membership_expiry - timezone.now().date()
            return delta.days
        return None

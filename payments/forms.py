from django import forms
from .models import Payment


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = [
            'member', 'plan', 'receipt_number', 'amount', 'discount',
            'status', 'method', 'coverage_from', 'coverage_to', 'paid_on', 'notes'
        ]
        widgets = {
            'coverage_from': forms.DateInput(attrs={'type': 'date'}),
            'coverage_to': forms.DateInput(attrs={'type': 'date'}),
            'paid_on': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 2}),
            'receipt_number': forms.TextInput(attrs={'placeholder': 'e.g. RCP-00001 (leave blank to auto-generate)'}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            from members.models import Member
            self.fields['member'].queryset = Member.objects.filter(
                branch__in=user.get_accessible_branches(), is_archived=False
            )
        self.fields['receipt_number'].required = False
        for f in self.fields.values():
            f.widget.attrs.setdefault('class', 'form-control')

    def clean_receipt_number(self):
        value = self.cleaned_data.get('receipt_number', '').strip()
        if value:
            # Check uniqueness only if a value was entered, excluding current instance on edit
            qs = Payment.objects.filter(receipt_number=value)
            if self.instance and self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError(f'Receipt number "{value}" is already used. Please enter a unique number.')
        return value

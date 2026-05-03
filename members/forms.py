from django import forms
from .models import Member


class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = [
            'branch', 'first_name', 'last_name', 'phone', 'email',
            'gender', 'date_of_birth', 'address', 'photo',
            'plan', 'membership_start', 'membership_expiry', 'notes',
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'membership_start': forms.DateInput(attrs={'type': 'date'}),
            'membership_expiry': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 2}),
            'notes': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user and not user.is_owner():
            self.fields['branch'].queryset = user.get_accessible_branches()
            self.fields['branch'].initial = user.branch
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', 'form-control')

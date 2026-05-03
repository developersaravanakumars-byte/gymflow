from django import forms
from .models import Enquiry


class EnquiryForm(forms.ModelForm):
    class Meta:
        model = Enquiry
        fields = ['branch', 'name', 'phone', 'email', 'source', 'interests', 'status', 'follow_up_date', 'notes']
        widgets = {
            'follow_up_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['branch'].queryset = user.get_accessible_branches()
        for f in self.fields.values():
            f.widget.attrs.setdefault('class', 'form-control')

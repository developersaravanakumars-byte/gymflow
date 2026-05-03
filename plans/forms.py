from django import forms
from .models import Plan
class PlanForm(forms.ModelForm):
    class Meta:
        model = Plan
        fields = ['name', 'description', 'duration', 'duration_unit', 'price', 'is_active']
        widgets = {'description': forms.Textarea(attrs={'rows': 2})}
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields.values():
            f.widget.attrs.setdefault('class', 'form-control')

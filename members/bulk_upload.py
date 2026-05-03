from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django import forms
import openpyxl
from .models import Member
from branches.models import Branch
from django.utils import timezone


class BulkUploadForm(forms.Form):
    branch = forms.ModelChoiceField(queryset=Branch.objects.filter(is_active=True))
    excel_file = forms.FileField(
        help_text='Upload .xlsx file. Columns: First Name, Last Name, Phone, Email'
    )

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['branch'].queryset = user.get_accessible_branches()
        for f in self.fields.values():
            f.widget.attrs.setdefault('class', 'form-control')


@login_required
def bulk_upload(request):
    if request.method == 'POST':
        form = BulkUploadForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            excel_file = request.FILES['excel_file']
            branch = form.cleaned_data['branch']
            try:
                wb = openpyxl.load_workbook(excel_file)
                ws = wb.active
                created = 0
                errors = []
                for row_num, row in enumerate(ws.iter_rows(min_row=2, values_only=True), 2):
                    first_name = str(row[0] or '').strip()
                    last_name = str(row[1] or '').strip()
                    phone = str(row[2] or '').strip()
                    email = str(row[3] or '').strip() if len(row) > 3 else ''

                    if not first_name or not phone:
                        errors.append(f'Row {row_num}: Missing first name or phone.')
                        continue

                    Member.objects.create(
                        branch=branch,
                        first_name=first_name,
                        last_name=last_name or '-',
                        phone=phone,
                        email=email,
                    )
                    created += 1

                messages.success(request, f'{created} members uploaded successfully.')
                if errors:
                    for e in errors[:5]:
                        messages.warning(request, e)
                return redirect('members:list')
            except Exception as e:
                messages.error(request, f'Error reading file: {e}')
    else:
        form = BulkUploadForm(user=request.user)

    return render(request, 'members/bulk_upload.html', {'form': form})

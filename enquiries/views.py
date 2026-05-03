from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Enquiry
from .forms import EnquiryForm


def get_branch_qs(user):
    return user.get_accessible_branches()


@login_required
def enquiry_list(request):
    qs = Enquiry.objects.filter(branch__in=get_branch_qs(request.user))
    status = request.GET.get('status', '')
    if status:
        qs = qs.filter(status=status)
    return render(request, 'enquiries/list.html', {'enquiries': qs, 'status': status})


@login_required
def enquiry_create(request):
    if request.method == 'POST':
        form = EnquiryForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Enquiry recorded.')
            return redirect('enquiries:list')
    else:
        form = EnquiryForm(user=request.user)
    return render(request, 'enquiries/form.html', {'form': form, 'title': 'New Enquiry'})


@login_required
def enquiry_detail(request, pk):
    enquiry = get_object_or_404(Enquiry, pk=pk, branch__in=get_branch_qs(request.user))
    return render(request, 'enquiries/detail.html', {'enquiry': enquiry})


@login_required
def enquiry_edit(request, pk):
    enquiry = get_object_or_404(Enquiry, pk=pk, branch__in=get_branch_qs(request.user))
    if request.method == 'POST':
        form = EnquiryForm(request.POST, instance=enquiry, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Enquiry updated.')
            return redirect('enquiries:detail', pk=pk)
    else:
        form = EnquiryForm(instance=enquiry, user=request.user)
    return render(request, 'enquiries/form.html', {'form': form, 'title': 'Edit Enquiry'})


@login_required
def enquiry_convert(request, pk):
    enquiry = get_object_or_404(Enquiry, pk=pk, branch__in=get_branch_qs(request.user))
    if request.method == 'POST':
        from members.models import Member
        member = Member.objects.create(
            branch=enquiry.branch,
            first_name=enquiry.name.split()[0],
            last_name=' '.join(enquiry.name.split()[1:]) or '-',
            phone=enquiry.phone,
            email=enquiry.email,
        )
        enquiry.status = 'converted'
        enquiry.converted_member = member
        enquiry.save()
        messages.success(request, f'{enquiry.name} converted to member.')
        return redirect('members:edit', pk=member.pk)
    return render(request, 'enquiries/confirm_convert.html', {'enquiry': enquiry})

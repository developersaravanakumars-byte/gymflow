from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from .models import Member
from .forms import MemberForm


def get_branch_filter(user):
    if user.is_owner():
        return {}
    return {'branch': user.branch}


@login_required
def dashboard(request):
    branch_filter = get_branch_filter(request.user)
    today = timezone.now().date()
    expiry_threshold = today + timezone.timedelta(days=7)

    context = {
        'total_members': Member.objects.filter(is_archived=False, **branch_filter).count(),
        'active_members': Member.objects.filter(
            is_archived=False, membership_expiry__gte=today, **branch_filter
        ).count(),
        'expiring_soon': Member.objects.filter(
            is_archived=False,
            membership_expiry__gte=today,
            membership_expiry__lte=expiry_threshold,
            **branch_filter
        ).count(),
        'recent_members': Member.objects.filter(
            is_archived=False, **branch_filter
        ).order_by('-joined_at')[:5],
    }
    return render(request, 'members/dashboard.html', context)


@login_required
def member_list(request):
    branch_filter = get_branch_filter(request.user)
    qs = Member.objects.filter(is_archived=False, **branch_filter)

    q = request.GET.get('q', '')
    if q:
        qs = qs.filter(
            Q(first_name__icontains=q) |
            Q(last_name__icontains=q) |
            Q(phone__icontains=q) |
            Q(email__icontains=q) |
            Q(member_id__icontains=q)
        )

    status = request.GET.get('status', '')
    today = timezone.now().date()
    if status == 'active':
        qs = qs.filter(membership_expiry__gte=today)
    elif status == 'expired':
        qs = qs.filter(membership_expiry__lt=today)

    return render(request, 'members/list.html', {'members': qs, 'q': q, 'status': status})


@login_required
def member_detail(request, pk):
    branch_filter = get_branch_filter(request.user)
    member = get_object_or_404(Member, pk=pk, **branch_filter)
    return render(request, 'members/detail.html', {'member': member})


@login_required
def member_create(request):
    if request.method == 'POST':
        form = MemberForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            member = form.save()
            messages.success(request, f'{member.full_name} added successfully.')
            return redirect('members:detail', pk=member.pk)
    else:
        form = MemberForm(user=request.user)
    return render(request, 'members/form.html', {'form': form, 'title': 'Add Member'})


@login_required
def member_edit(request, pk):
    branch_filter = get_branch_filter(request.user)
    member = get_object_or_404(Member, pk=pk, **branch_filter)
    if request.method == 'POST':
        form = MemberForm(request.POST, request.FILES, instance=member, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Member updated successfully.')
            return redirect('members:detail', pk=member.pk)
    else:
        form = MemberForm(instance=member, user=request.user)
    return render(request, 'members/form.html', {'form': form, 'title': 'Edit Member', 'member': member})


@login_required
def member_archive(request, pk):
    branch_filter = get_branch_filter(request.user)
    member = get_object_or_404(Member, pk=pk, **branch_filter)
    if request.method == 'POST':
        member.is_archived = True
        member.save()
        messages.success(request, f'{member.full_name} archived.')
        return redirect('members:list')
    return render(request, 'members/confirm_archive.html', {'member': member})


@login_required
def archived_list(request):
    branch_filter = get_branch_filter(request.user)
    members = Member.objects.filter(is_archived=True, **branch_filter)
    return render(request, 'members/archived.html', {'members': members})


@login_required
def member_restore(request, pk):
    branch_filter = get_branch_filter(request.user)
    member = get_object_or_404(Member, pk=pk, is_archived=True, **branch_filter)
    if request.method == 'POST':
        member.is_archived = False
        member.save()
        messages.success(request, f'{member.full_name} restored.')
        return redirect('members:list')
    return render(request, 'members/confirm_restore.html', {'member': member})

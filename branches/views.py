from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import Branch

@login_required
def branch_list(request):
    branches = request.user.get_accessible_branches()
    return render(request, 'branches/list.html', {'branches': branches})

@login_required
def branch_detail(request, pk):
    branch = get_object_or_404(Branch, pk=pk)
    return render(request, 'branches/detail.html', {'branch': branch})

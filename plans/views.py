from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Plan
from .forms import PlanForm

@login_required
def plan_list(request):
    plans = Plan.objects.filter(is_active=True)
    return render(request, 'plans/list.html', {'plans': plans})

@login_required
def plan_create(request):
    if request.method == 'POST':
        form = PlanForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Plan created.')
            return redirect('plans:list')
    else:
        form = PlanForm()
    return render(request, 'plans/form.html', {'form': form, 'title': 'Add Plan'})

@login_required
def plan_edit(request, pk):
    plan = get_object_or_404(Plan, pk=pk)
    if request.method == 'POST':
        form = PlanForm(request.POST, instance=plan)
        if form.is_valid():
            form.save()
            messages.success(request, 'Plan updated.')
            return redirect('plans:list')
    else:
        form = PlanForm(instance=plan)
    return render(request, 'plans/form.html', {'form': form, 'title': 'Edit Plan'})

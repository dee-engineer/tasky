from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import Task, User
from .forms import TaskForm, UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.http import require_POST


@login_required
def home(request):
    query = request.GET.get('q')
    sort_by = request.GET.get('sort_by', '')
    filter_by = request.GET.get('filter_by', 'all')
    preview_by = request.GET.get('preview_by', '')

    # Initial queryset for tasks
    tasks = Task.objects.all()

    # Filter tasks based on status
    if filter_by == 'in_progress':
        tasks = tasks.filter(status='in_progress')
    elif filter_by == 'completed':
        tasks = tasks.filter(status='completed')
    elif filter_by == 'overdue':
        tasks = tasks.filter(status='overdue')

    # Search tasks by query parameter
    if query:
        tasks = tasks.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(category__icontains=query)
        )

    # Sort tasks based on sort_by parameter
    if sort_by == 'priority':
        tasks = tasks.order_by('priority')
    elif sort_by == 'due_date':
        tasks = tasks.order_by('due_date')
    elif sort_by == 'category':
        tasks = tasks.order_by('category')

    # Handle preview functionality
    if preview_by == 'task_summary':
        tasks = tasks.values('title', 'status', 'priority', 'due_date')  # Display only summary info
    elif preview_by == 'task_detail':
        tasks = tasks.values('title', 'description', 'status', 'priority', 'due_date', 'category')  # Display detailed info

    # Retrieve all users
    users = User.objects.all()
    in_progress_tasks = Task.objects.filter(status='in_progress')
    completed_tasks = Task.objects.filter(status='completed')
    overdue_tasks = Task.objects.filter(status='overdue')

    # Count tasks for each status
    inprogress_count = Task.objects.filter(status='in_progress').count()
    completed_count = Task.objects.filter(status='completed').count()
    overdue_count = Task.objects.filter(status='overdue').count()

    context = {
        'in_progress_tasks': in_progress_tasks,
        'completed_tasks': completed_tasks,
        'overdue_tasks': overdue_tasks,
        'query': query,
        'users': users,
        'inprogress_count': inprogress_count,
        'completed_count': completed_count,
        'overdue_count': overdue_count,
    }

    return render(request, 'index.html', context)


@login_required
def tasks(request):
    query = request.GET.get('q')
    tasks = Task.objects.all()

    if query:
        tasks = tasks.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(category__icontains=query)
        )

    return render(request, 'tasks.html', {'tasks': tasks, 'query': query})


@login_required
def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = TaskForm()
    return render(request, 'add_task.html', {'form': form})


@login_required
def members(request):
    users = User.objects.all()
    return render(request, 'members.html', {'users': users})


@login_required
def create_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('members')
    else:
        form = UserCreationForm()
    return render(request, 'add_members.html', {'form': form})


@login_required
def edit_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save(commit=False)
            if not task.due_date:
                task.due_date = None
            task.save()
            form.save_m2m()
            return redirect('home')
        else:
            print(form.errors)
    else:
        form = TaskForm(instance=task)
    return render(request, 'edit_task.html', {'form': form, 'task': task})


@login_required
def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.delete()
    return redirect('home')


@require_POST
def update_task_status(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    new_status = request.POST.get('status')
    
    if new_status:
        task.status = new_status
        task.save()
        return JsonResponse({'message': 'Task status updated successfully'})
    else:
        return JsonResponse({'error': 'Invalid status provided'}, status=400)


def login_user(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
            error = "Invalid username or password."
            return render(request, 'login.html', {'error': error})

    return render(request, 'login.html')


@login_required
def logout_user(request):
    logout(request)
    return redirect('login')
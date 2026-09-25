from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import ProtectedError
from .models import Task, Category, Priority, Note, Activity
from .forms import TaskForm, NoteForm, LoginForm, CategoryForm, PriorityForm


def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            login(request, form.get_user())
            return redirect("dashboard")
    else:
        form = LoginForm()

    return render(request, "tasks/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("login")


@login_required(login_url="login")
def dashboard(request):
    tasks = Task.objects.all().order_by("-created_at")
    total_tasks = Task.objects.count()
    pending_tasks = Task.objects.filter(status="Pending").count()
    completed_tasks = Task.objects.filter(status="Completed").count()

    return render(request, "tasks/dashboard.html", {
        "tasks": tasks,
        "total_tasks": total_tasks,
        "pending_tasks": pending_tasks,
        "completed_tasks": completed_tasks,
    })


@login_required(login_url="login")
def task_list(request):
    search = request.GET.get("q", "")
    tasks = Task.objects.all().order_by("-created_at")

    if search:
        tasks = tasks.filter(title__icontains=search)

    return render(request, "tasks/tasks.html", {
        "tasks": tasks,
        "search": search
    })


@login_required(login_url="login")
def add_task(request):
    if request.method == "POST":
        form = TaskForm(request.POST)

        if form.is_valid():
            task = form.save()

            Activity.objects.create(
                user=request.user,
                message=f'Added task "{task.title}"'
            )

            return redirect("task_list")
    else:
        form = TaskForm()

    return render(request, "tasks/add_task.html", {"form": form})


@login_required(login_url="login")
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)

        if form.is_valid():
            task = form.save()

            Activity.objects.create(
                user=request.user,
                message=f'Edited task "{task.title}"'
            )

            return redirect("task_list")
    else:
        form = TaskForm(instance=task)

    return render(request, "tasks/edit_task.html", {
        "form": form,
        "task": task
    })


@login_required(login_url="login")
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == "POST":
        task_title = task.title
        task.delete()

        Activity.objects.create(
            user=request.user,
            message=f'Deleted task "{task_title}"'
        )

        return redirect("task_list")

    return redirect("task_list")


@login_required(login_url="login")
def add_note(request):
    if request.method == "POST":
        form = NoteForm(request.POST)

        if form.is_valid():
            note = form.save()

            Activity.objects.create(
                user=request.user,
                message=f'Added a note to "{note.task.title}"'
            )

            return redirect("note_list")
    else:
        form = NoteForm()

    return render(request, "tasks/add_note.html", {"form": form})


@login_required(login_url="login")
def delete_note(request, note_id):
    note = get_object_or_404(Note, id=note_id)

    if request.method == "POST":
        task_title = note.task.title

        note.delete()

        Activity.objects.create(
            user=request.user,
            message=f'Deleted a note from "{task_title}"'
        )

    return redirect("note_list")


@login_required(login_url="login")
def category_list(request):
    categories = Category.objects.all().order_by("name")

    return render(request, "tasks/categories.html", {
        "categories": categories
    })


@login_required(login_url="login")
def add_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)

        if form.is_valid():
            category = form.save()

            Activity.objects.create(
                user=request.user,
                message=f'Added category "{category.name}"'
            )

            return redirect("category_list")
    else:
        form = CategoryForm()

    return render(request, "tasks/add_category.html", {"form": form})


@login_required(login_url="login")
def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)

    if request.method == "POST":
        category_name = category.name

        try:
            category.delete()

            Activity.objects.create(
                user=request.user,
                message=f'Deleted category "{category_name}"'
            )

        except ProtectedError:
            pass

    return redirect("category_list")


@login_required(login_url="login")
def priority_list(request):
    priorities = Priority.objects.all().order_by("name")

    return render(request, "tasks/priorities.html", {
        "priorities": priorities
    })


@login_required(login_url="login")
def add_priority(request):
    if request.method == "POST":
        form = PriorityForm(request.POST)

        if form.is_valid():
            priority = form.save()

            Activity.objects.create(
                user=request.user,
                message=f'Added priority "{priority.name}"'
            )

            return redirect("priority_list")
    else:
        form = PriorityForm()

    return render(request, "tasks/add_priority.html", {"form": form})


@login_required(login_url="login")
def delete_priority(request, priority_id):
    priority = get_object_or_404(Priority, id=priority_id)

    if request.method == "POST":
        priority_name = priority.name

        try:
            priority.delete()

            Activity.objects.create(
                user=request.user,
                message=f'Deleted priority "{priority_name}"'
            )

        except ProtectedError:
            pass

    return redirect("priority_list")


@login_required(login_url="login")
def note_list(request):
    notes = Note.objects.all().order_by("-created_at")

    return render(request, "tasks/notes.html", {
        "notes": notes
    })


@login_required(login_url="login")
def activity_list(request):
    activities = Activity.objects.filter(
        user=request.user
    ).order_by("-created_at")

    latest_activity = activities.first()

    if latest_activity:
        request.session["activity_seen_id"] = latest_activity.id

    return render(request, "tasks/activity.html", {
        "activities": activities
    })


@login_required(login_url="login")
def delete_activity(request, activity_id):
    activity = get_object_or_404(
        Activity,
        id=activity_id,
        user=request.user
    )

    if request.method == "POST":
        activity.delete()

    return redirect("activity_list")


@login_required(login_url="login")
def clear_activities(request):
    if request.method == "POST":
        Activity.objects.filter(user=request.user).delete()
        request.session["activity_seen_id"] = 0

    return redirect("activity_list")
from django.shortcuts import render, redirect, get_object_or_404
from .models import Task, Category, Priority, Note
from .forms import TaskForm, NoteForm


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


def task_list(request):
    tasks = Task.objects.all().order_by("-created_at")
    return render(request, "tasks/tasks.html", {"tasks": tasks})


def add_task(request):
    if request.method == "POST":
        form = TaskForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("task_list")
    else:
        form = TaskForm()

    return render(request, "tasks/add_task.html", {"form": form})


def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)

        if form.is_valid():
            form.save()
            return redirect("task_list")
    else:
        form = TaskForm(instance=task)

    return render(request, "tasks/edit_task.html", {
        "form": form,
        "task": task,
    })


def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == "POST":
        task.delete()
        return redirect("task_list")

    return redirect("task_list")


def add_note(request):
    if request.method == "POST":
        form = NoteForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("note_list")
    else:
        form = NoteForm()

    return render(request, "tasks/add_note.html", {"form": form})


def category_list(request):
    categories = Category.objects.all().order_by("name")
    return render(request, "tasks/categories.html", {"categories": categories})


def priority_list(request):
    priorities = Priority.objects.all().order_by("name")
    return render(request, "tasks/priorities.html", {"priorities": priorities})


def note_list(request):
    notes = Note.objects.all().order_by("-created_at")
    return render(request, "tasks/notes.html", {"notes": notes})